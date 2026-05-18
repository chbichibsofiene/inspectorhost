package com.inspector.platform.service.impl;

import com.inspector.platform.service.EmailService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@Slf4j
public class EmailServiceImpl implements EmailService {

    private final String fromEmail;
    private final String brevoApiKey;
    private final RestTemplate restTemplate;
    
    private static final String BREVO_API_URL = "https://api.brevo.com/v3/smtp/email";

    public EmailServiceImpl(
            @Value("${spring.mail.username}") String fromEmail,
            @Value("${app.brevo.api-key:}") String brevoApiKey) {
        this.fromEmail = fromEmail;
        this.brevoApiKey = brevoApiKey;
        this.restTemplate = new RestTemplate();
    }

    private String buildEmailTemplate(String title, String body, String actionText, String actionUrl) {
        String actionButton = "";
        if (actionText != null && actionUrl != null) {
            actionButton = String.format(
                    "      <div style='margin: 40px 0; text-align: center;'>" +
                            "        <a href='%s' style='background: #1a56db; color: #ffffff; padding: 14px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px; display: inline-block; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>%s</a>"
                            +
                            "      </div>",
                    actionUrl, actionText);
        }

        // Removed the inline CID logo and replaced with a hosted education logo, 
        // as Brevo HTTP API inline attachments are slightly different than JavaMailSender
        return String.format(
                "<!DOCTYPE html><html>" +
                        "<head>" +
                        "  <style>body { margin: 0; padding: 0; -webkit-text-size-adjust: 100%%; -ms-text-size-adjust: 100%%; }</style>"
                        +
                        "</head>" +
                        "<body style='margin: 0; padding: 0; background-color: #f9fafb; font-family: \"Inter\", \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif;'>"
                        +
                        "  <table role='presentation' width='100%%' cellspacing='0' cellpadding='0' border='0'>" +
                        "    <tr>" +
                        "      <td align='center' style='padding: 0;'>" +
                        "        <table role='presentation' width='600' cellspacing='0' cellpadding='0' border='0' style='background-color: #ffffff; margin-top: 40px; margin-bottom: 40px; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);'>"
                        +
                        "          <tr>" +
                        "            <td align='center' style='background-color: #1e3a8a; padding: 40px 0;'>" +
                        "              <img src='https://cdn-icons-png.flaticon.com/512/330/330996.png' alt='Pedagogy Center' style='height: 60px; display: block; filter: brightness(0) invert(1);'>"
                        +
                        "            </td>" +
                        "          </tr>" +
                        "          <!-- Body -->" +
                        "          <tr>" +
                        "            <td style='padding: 50px 50px 40px 50px;'>" +
                        "              <h1 style='margin: 0 0 30px 0; font-size: 32px; font-weight: 800; color: #111827; line-height: 1.2; text-align: center; letter-spacing: -0.025em;'>%s</h1>"
                        +
                        "              <div style='font-size: 16px; color: #4b5563; line-height: 1.7; text-align: center;'>"
                        +
                        "                %s" +
                        "              </div>" +
                        "              %s" +
                        "            </td>" +
                        "          </tr>" +
                        "          <!-- Footer -->" +
                        "          <tr>" +
                        "            <td align='center' style='padding: 40px; background-color: #f3f4f6; border-top: 1px solid #e5e7eb;'>"
                        +
                        "              <div style='margin-bottom: 20px;'>" +
                        "                <a href='https://www.facebook.com/cnteducation/?locale=fr_FR' style='margin: 0 10px;'><img src='https://cdn-icons-png.flaticon.com/512/733/733547.png' width='24' style='opacity: 0.6;'></a>"
                        +
                        "              </div>" +
                        "              <div href='https://www.cnte.tn/' style='font-size: 14px; color: #6b7280; font-weight: 500; margin-bottom: 8px;'>www.cnte.tn</div>"
                        +
                        "              <div style='font-size: 12px; color: #9ca3af; margin-bottom: 12px;'>*Pedagogy Center</div>"
                        +
                        "              <div style='font-size: 12px; color: #9ca3af;'>&copy; 2026 Pedagogy Center. All Rights Reserved.</div>"
                        +
                        "            </td>" +
                        "          </tr>" +
                        "        </table>" +
                        "      </td>" +
                        "    </tr>" +
                        "  </table>" +
                        "</body>" +
                        "</html>",
                title, body, actionButton);
    }
    
    private void sendViaBrevo(String to, String name, String subject, String htmlContent) {
        if (brevoApiKey == null || brevoApiKey.isEmpty()) {
            log.error("Brevo API key is missing. Cannot send email to {}", to);
            return;
        }

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("api-key", brevoApiKey);
            headers.set("accept", "application/json");

            Map<String, Object> body = new HashMap<>();
            
            Map<String, String> sender = new HashMap<>();
            sender.put("name", "Pedagogy Center");
            sender.put("email", fromEmail);
            body.put("sender", sender);

            Map<String, String> recipient = new HashMap<>();
            recipient.put("email", to);
            if (name != null && !name.isEmpty()) {
                recipient.put("name", name);
            }
            body.put("to", List.of(recipient));

            body.put("subject", subject);
            body.put("htmlContent", htmlContent);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);

            ResponseEntity<String> response = restTemplate.exchange(
                    BREVO_API_URL,
                    HttpMethod.POST,
                    entity,
                    String.class
            );

            log.info("Email sent successfully via Brevo to {}. Response code: {}", to, response.getStatusCode());
        } catch (Exception e) {
            log.error("Failed to send email via Brevo HTTP API: {}", e.getMessage(), e);
        }
    }

    @Override
    @Async
    public void sendAccountVerificationEmail(String to, String name) {
        log.info("Sending account verification email to {}", to);
        String subject = "Account Verified - Pedagogy Center";
        String bodyText = String.format(
                "Hello <strong>%s</strong>,<br><br>" +
                        "Great news! Your account has been <strong>successfully verified</strong> by our administration team. "
                        +
                        "You now have full access to the Inspector Platform features and resources.",
                name);
        // Uses relative path if frontend is hosted together, or full path if separate
        String content = buildEmailTemplate("Account Verified. Welcome onboard.", bodyText, "Login to Dashboard", "https://inspector-1-main-frontend.vercel.app/login"); // Update URL to match your real frontend
        sendViaBrevo(to, name, subject, content);
    }

    @Override
    @Async
    public void sendRegistrationEmail(String to, String name) {
        log.info("Sending registration confirmation email to {}", to);
        String subject = "Welcome to Inspector Platform - Registration Successful";
        String bodyText = String.format(
                "Hello <strong>%s</strong>,<br><br>" +
                        "Thank you for joining the <strong>Inspector Platform</strong>. Your registration has been received successfully.<br><br>"
                        +
                        "Our administration team will review your credentials shortly. You will receive another notification once your account is activated.",
                name);
        String content = buildEmailTemplate("Registration Received!", bodyText, null, null);
        sendViaBrevo(to, name, subject, content);
    }

    @Override
    @Async
    public void sendGenericNotificationEmail(String to, String name, String title, String messageContent, String actionUrl) {
        log.info("Sending generic notification email to {}", to);
        String subject = title + " - Pedagogy Center";
        // Ensure action URL uses absolute URL to your frontend
        String fullActionUrl = actionUrl.startsWith("http") ? actionUrl : "https://inspector-1-main-frontend.vercel.app" + (actionUrl.startsWith("/") ? actionUrl : "/" + actionUrl);
        String bodyText = String.format("Hello <strong>%s</strong>,<br><br>%s", name, messageContent);
        String content = buildEmailTemplate(title, bodyText, "View Details", fullActionUrl);
        sendViaBrevo(to, name, subject, content);
    }

    @Override
    @Async
    public void sendPasswordResetEmail(String to, String name, String code) {
        log.info("Sending password reset email to {}", to);
        String subject = "Password Reset Request - Pedagogy Center";
        String bodyText = String.format(
                "Hello <strong>%s</strong>,<br><br>" +
                        "To reset your password, please use the verification code below. This code will expire in 15 minutes.<br><br>"
                        +
                        "<div style='background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;'>"
                        +
                        "  <span style='font-size: 32px; font-weight: 800; letter-spacing: 0.3em; color: #1a56db;'>%s</span>"
                        +
                        "</div>",
                name, code);
        String content = buildEmailTemplate("Reset Your Password", bodyText, null, null);
        sendViaBrevo(to, name, subject, content);
    }

    @Override
    @Async
    public void sendSimpleEmail(String to, String subject, String bodyText) {
        log.info("Sending simple styled email to {}", to);
        String content = buildEmailTemplate(subject, bodyText, null, null);
        sendViaBrevo(to, null, subject, content);
    }
}
