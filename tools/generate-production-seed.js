const fs = require("fs");
const path = require("path");

const out = path.resolve(__dirname, "..", "backend", "src", "main", "resources", "production_demo_seed.sql");
const hash = "$2a$10$pWUTXsoXtLSdNrCjT64JuOMviCF5i6i7ywRD8OPT7/4C4NxnTeoHK"; // password123

const subjects = ["ARABIC", "FRENCH", "ENGLISH", "MATH", "PHYSICS", "CHEMISTRY", "BIOLOGY", "HISTORY_GEOGRAPHY", "PHILOSOPHY", "ISLAMIC_STUDIES", "PHYSICAL_EDUCATION", "COMPUTER_SCIENCE", "ECONOMICS", "ARTS", "MUSIC"];
const subjectLabels = {
  ARABIC: "Arabe", FRENCH: "Francais", ENGLISH: "Anglais", MATH: "Mathematiques",
  PHYSICS: "Physique", CHEMISTRY: "Chimie", BIOLOGY: "Sciences de la vie",
  HISTORY_GEOGRAPHY: "Histoire-Geographie", PHILOSOPHY: "Philosophie",
  ISLAMIC_STUDIES: "Education islamique", PHYSICAL_EDUCATION: "Education physique",
  COMPUTER_SCIENCE: "Informatique", ECONOMICS: "Economie", ARTS: "Arts plastiques", MUSIC: "Musique"
};
const levels = ["PRIMARY", "PREPARATORY", "SECONDARY"];
const regions = [
  ["Tunis", ["Tunis Medina", "Bab Bhar", "Carthage"]],
  ["Ariana", ["Ariana Ville", "La Soukra", "Mnihla"]],
  ["Ben Arous", ["Ben Arous", "Rades", "Hammam Lif"]],
  ["Manouba", ["Manouba", "Douar Hicher", "Tebourba"]],
  ["Nabeul", ["Nabeul", "Hammamet", "Korba"]],
  ["Bizerte", ["Bizerte Nord", "Menzel Bourguiba", "Ras Jebel"]],
  ["Beja", ["Beja Nord", "Medjez El Bab", "Testour"]],
  ["Jendouba", ["Jendouba", "Tabarka", "Ain Draham"]],
  ["Kef", ["Le Kef", "Tajerouine", "Dahmani"]],
  ["Siliana", ["Siliana Nord", "Gaafour", "Makthar"]],
  ["Sousse", ["Sousse Ville", "Msaken", "Akouda"]],
  ["Monastir", ["Monastir", "Moknine", "Jemmal"]],
  ["Mahdia", ["Mahdia", "Ksour Essef", "Chebba"]],
  ["Sfax", ["Sfax Ville", "Sakiet Ezzit", "Menzel Chaker"]],
  ["Kairouan", ["Kairouan Nord", "Haffouz", "Oueslatia"]],
  ["Kasserine", ["Kasserine Nord", "Sbeitla", "Feriana"]],
  ["Sidi Bouzid", ["Sidi Bouzid Ouest", "Regueb", "Meknassy"]],
  ["Gabes", ["Gabes Ville", "Mareth", "El Hamma"]],
  ["Medenine", ["Medenine Nord", "Djerba Houmt Souk", "Zarzis"]],
  ["Tataouine", ["Tataouine Nord", "Ghomrassen", "Remada"]],
  ["Gafsa", ["Gafsa Nord", "Metlaoui", "Redeyef"]],
  ["Tozeur", ["Tozeur", "Nefta", "Degache"]],
  ["Kebili", ["Kebili Sud", "Douz", "Souk Lahad"]],
  ["Zaghouan", ["Zaghouan", "El Fahs", "Nadhour"]]
];
const firstNames = ["Mohamed", "Ahmed", "Youssef", "Sami", "Anis", "Walid", "Karim", "Mehdi", "Nizar", "Hatem", "Sofiene", "Tarek", "Mourad", "Ridha", "Imed", "Fatma", "Amel", "Leila", "Sarra", "Mouna", "Nadia", "Rim", "Emna", "Ines", "Aicha", "Hela", "Olfa", "Asma", "Mariem", "Wafa"];
const lastNames = ["Ben Ali", "Trabelsi", "Mansouri", "Jlassi", "Gharbi", "Bouzid", "Mabrouk", "Khemiri", "Mejri", "Baccouche", "Hamdi", "Ayari", "Zouari", "Saidi", "Chakroun", "Karray", "Haddad", "Gharsalli", "Nasri", "Sellami", "Abid", "Masmoudi", "Cherif", "Dridi", "Ben Salem"];
const schoolPrefixes = ["Ecole primaire", "College", "Lycee", "Institut pilote"];
const schoolNames = ["Ibn Khaldoun", "Habib Bourguiba", "Farhat Hached", "Ali Belhouane", "Les Jasmins", "El Amal", "Carthage", "El Manar", "Taher Haddad", "Abou Kacem Chebbi", "Avenue de la Republique", "El Mourouj"];

let sql = [];
const rows = (table, cols, data) => {
  if (!data.length) return;
  sql.push(`INSERT INTO ${table} (${cols.join(", ")}) VALUES`);
  sql.push(data.map(r => `(${r.join(", ")})`).join(",\n") + ";");
};
const q = v => v === null ? "NULL" : `'${String(v).replace(/\\/g, "\\\\").replace(/'/g, "''")}'`;
const dt = days => `DATE_ADD(NOW(), INTERVAL ${days} DAY)`;
const date = days => `DATE(DATE_ADD(NOW(), INTERVAL ${days} DAY))`;
const pick = (arr, i) => arr[i % arr.length];

sql.push("SET FOREIGN_KEY_CHECKS=0;");
["lesson_progress","course_assignments","course_lessons","course_modules","courses","quiz_submissions","quiz_assignments","quiz_questions","quizzes","messages","conversations","notifications","activity_reports","activity_guests","activities","inspections","action_logs","timetable_slots","profile_etablissements","profile_departments","profile_dependencies","profile_delegations","teacher_profiles","inspector_profiles","personnel","users","etablissements","dependencies","departments","delegations","regions"].forEach(t => sql.push(`TRUNCATE TABLE ${t};`));
sql.push("SET FOREIGN_KEY_CHECKS=1;");

rows("regions", ["id", "name"], regions.map((r, i) => [i + 1, q(r[0])]));
let delegations = [];
regions.forEach((r, ri) => r[1].forEach(d => delegations.push({ name: d, regionId: ri + 1 })));
rows("delegations", ["id", "name", "region_id"], delegations.map((d, i) => [i + 1, q(d.name), d.regionId]));
rows("departments", ["id", "name", "delegation_id"], delegations.flatMap((d, i) => subjects.slice(0, 8).map((s, j) => [i * 8 + j + 1, q(subjectLabels[s]), i + 1])));
rows("dependencies", ["id", "name", "delegation_id"], delegations.flatMap((d, i) => [[i * 2 + 1, q(`Circonscription ${d.name} Nord`), i + 1], [i * 2 + 2, q(`Circonscription ${d.name} Sud`), i + 1]]));
rows("etablissements", ["id", "name", "school_level", "dependency_id"], Array.from({ length: delegations.length * 4 }, (_, i) => [i + 1, q(`${pick(schoolPrefixes, i)} ${pick(schoolNames, i)} - ${delegations[Math.floor(i / 4)].name}`), q(pick(levels, i)), Math.floor(i / 2) + 1]));

const users = [];
for (let i = 1; i <= 100; i++) {
  const role = i <= 3 ? "ADMIN" : i <= 20 ? "INSPECTOR" : "TEACHER";
  const fn = pick(firstNames, i * 3);
  const ln = pick(lastNames, i * 5);
  const serial = `${role.slice(0, 5)}-${String(2026 - (i % 18)).padStart(4, "0")}-${String(i).padStart(4, "0")}`;
  users.push({ id: i, role, fn, ln, serial, cin: String(10000000 + i), email: `${fn}.${ln}`.toLowerCase().replace(/ /g, ".") + `${i}@inspection.tn` });
}
users[0].email = "admin@example.com";
rows("personnel", ["id", "cin", "first_name", "last_name", "recruitment_date", "role", "serial_code"], users.map(u => [u.id, q(u.cin), q(u.fn), q(u.ln), q(`20${10 + (u.id % 14)}-${String((u.id % 12) + 1).padStart(2, "0")}-15`), q(u.role), q(u.serial)]));
rows("users", ["id", "created_at", "email", "enabled", "password", "profile_completed", "role", "serial_code"], users.map(u => [u.id, dt(-220 + u.id), q(u.email), 1, q(hash), 1, q(u.role), q(u.serial)]));

const inspectors = users.filter(u => u.role === "INSPECTOR");
const teachers = users.filter(u => u.role === "TEACHER");
rows("inspector_profiles", ["id", "first_name", "last_name", "rank", "subject", "school_level", "phone", "language", "user_id"], inspectors.map((u, i) => [i + 1, q(u.fn), q(u.ln), q(pick(["INSPECTOR", "INSPECTOR_PRINCIPAL", "INSPECTOR_REGIONAL", "INSPECTOR_GENERAL"], i)), q(pick(subjects, i)), q(pick(levels, i)), q(`+216 2${i % 8} ${String(100000 + i * 137).slice(0, 6)}`), q(pick(["ar", "fr"], i)), u.id]));
rows("teacher_profiles", ["id", "first_name", "last_name", "subject", "phone", "language", "delegation_id", "dependency_id", "etablissement_id", "user_id"], teachers.map((u, i) => {
  const del = (i % delegations.length) + 1;
  return [i + 1, q(u.fn), q(u.ln), q(pick(subjects, i)), q(`+216 5${i % 8} ${String(200000 + i * 211).slice(0, 6)}`), q(pick(["ar", "fr"], i + 1)), del, (del - 1) * 2 + (i % 2) + 1, (del - 1) * 4 + (i % 4) + 1, u.id];
}));
rows("profile_delegations", ["profile_id", "delegation_id"], inspectors.flatMap((_, i) => [1, 2, 3].map(off => [i + 1, ((i * 4 + off) % delegations.length) + 1])));
rows("profile_departments", ["profile_id", "department_id"], inspectors.flatMap((_, i) => [1, 2].map(off => [i + 1, (((i * 4 + off) % delegations.length) * 8) + (i % 8) + 1])));
rows("profile_dependencies", ["profile_id", "dependency_id"], inspectors.flatMap((_, i) => [1, 2].map(off => [i + 1, ((i * 5 + off) % (delegations.length * 2)) + 1])));
rows("profile_etablissements", ["profile_id", "etablissement_id"], inspectors.flatMap((_, i) => {
  const inspectorSubject = pick(subjects, i);
  const schools = teachers
    .map((teacher, teacherIndex) => ({
      subject: pick(subjects, teacherIndex),
      etablissementId: (((teacherIndex % delegations.length) + 1) - 1) * 4 + (teacherIndex % 4) + 1
    }))
    .filter(teacher => teacher.subject === inspectorSubject)
    .map(teacher => teacher.etablissementId);
  return [...new Set(schools)].slice(0, 4).map(etablissementId => [i + 1, etablissementId]);
}));

rows("activities", ["id", "description", "end_date_time", "is_online", "is_reminder_sent", "location", "meeting_url", "start_date_time", "title", "type", "inspector_user_id"], Array.from({ length: 150 }, (_, i) => {
  const online = i % 6 === 0;
  const type = pick(["INSPECTION", "VISITE_PEDAGOGIQUE", "FORMATION", "REUNION_TRAVAIL", "LECON_TEMOIN", "SEMINAIRE"], i);
  return [i + 1, q(`Suivi pedagogique et accompagnement des enseignants - dossier ${i + 1}`), dt(-90 + i), online ? 1 : 0, i < 105 ? 1 : 0, q(online ? "En ligne" : `${pick(schoolNames, i)} - ${pick(regions, i)[0]}`), online ? q(`https://meet.jit.si/Inspector-demo-${i + 1}`) : "NULL", dt(-90 + i), q(`${type.replace(/_/g, " ")} ${pick(subjects, i)}`), q(type), inspectors[i % inspectors.length].id];
}));
rows("activity_guests", ["activity_id", "teacher_profile_id"], Array.from({ length: 300 }, (_, i) => [(i % 150) + 1, (i * 7 % teachers.length) + 1]));
rows("activity_reports", ["id", "created_at", "observations", "recommendations", "score", "status", "title", "updated_at", "activity_id", "inspector_user_id", "teacher_profile_id"], Array.from({ length: 95 }, (_, i) => [i + 1, dt(-85 + i), q(`Observation: classe bien geree, progression conforme au programme, participation elevee des eleves. Points de vigilance notes pendant la visite ${i + 1}.`), q(`Recommandations: renforcer l'evaluation formative, varier les supports numeriques, planifier une remediation ciblee.`), 10 + (i % 11), q(i % 5 === 0 ? "DRAFT" : "FINAL"), q(`Rapport pedagogique ${i + 1}`), dt(-84 + i), i + 1, inspectors[i % inspectors.length].id, (i * 3 % teachers.length) + 1]));
rows("inspections", ["id", "created_at", "score", "delegation_id", "inspector_user_id"], Array.from({ length: 120 }, (_, i) => [i + 1, dt(-120 + i), 9 + (i % 12), (i % delegations.length) + 1, inspectors[i % inspectors.length].id]));

rows("courses", ["id", "created_at", "description", "status", "subject", "title", "updated_at", "inspector_id"], Array.from({ length: 20 }, (_, i) => [i + 1, dt(-80 + i), q("Parcours de formation continue avec ressources, activites pratiques et evaluation."), q(i % 4 === 0 ? "DRAFT" : "PUBLISHED"), q(pick(subjects, i)), q(`Formation ${subjectLabels[pick(subjects, i)]} - sequence ${i + 1}`), dt(-70 + i), (i % inspectors.length) + 1]));
rows("course_modules", ["id", "description", "order_index", "title", "course_id"], Array.from({ length: 60 }, (_, i) => [i + 1, q("Objectifs, supports et activites d'application."), (i % 3) + 1, q(`Module ${(i % 3) + 1}`), Math.floor(i / 3) + 1]));
rows("course_lessons", ["id", "content_url", "description", "duration_minutes", "order_index", "title", "type", "module_id"], Array.from({ length: 180 }, (_, i) => [i + 1, q(`/resources/courses/lesson-${i + 1}`), q("Ressource pedagogique structuree pour la formation."), 20 + (i % 40), (i % 3) + 1, q(`Lecon ${(i % 3) + 1}`), q(pick(["PDF", "VIDEO", "QUIZ"], i)), Math.floor(i / 3) + 1]));
const courseAssignments = [];
for (let c = 1; c <= 20; c++) for (let j = 0; j < 8; j++) courseAssignments.push([courseAssignments.length + 1, dt(-60 + c + j), c, ((c * 5 + j) % teachers.length) + 1]);
rows("course_assignments", ["id", "assigned_at", "course_id", "teacher_id"], courseAssignments);
rows("lesson_progress", ["id", "completed", "completed_at", "score", "lesson_id", "teacher_id"], courseAssignments.slice(0, 260).map((a, i) => [i + 1, i % 4 === 0 ? 0 : 1, i % 4 === 0 ? "NULL" : dt(-35 + (i % 50)), i % 3 === 0 ? 12 + (i % 9) : "NULL", ((a[2] - 1) * 9 + (i % 9)) + 1, a[3]]));

rows("quizzes", ["id", "created_at", "grade", "school_level", "subject", "title", "topic", "inspector_id"], Array.from({ length: 25 }, (_, i) => [i + 1, dt(-65 + i), q(pick(["6eme", "7eme", "8eme", "9eme", "1ere secondaire", "2eme secondaire", "Bac"], i)), q(pick(levels, i)), q(pick(subjects, i)), q(`Quiz diagnostic ${subjectLabels[pick(subjects, i)]} ${i + 1}`), q(pick(["Evaluation formative", "Competences de base", "Remediation", "Integration des TIC"], i)), (i % inspectors.length) + 1]));
rows("quiz_questions", ["id", "correct_answer", "options", "question_text", "type", "quiz_id"], Array.from({ length: 100 }, (_, i) => [i + 1, q(i % 2 === 0 ? "B" : "Reponse argumentee attendue"), i % 2 === 0 ? q('["A","B","C","D"]') : "NULL", q(`Question ${i + 1}: analyser la situation pedagogique proposee.`), q(i % 2 === 0 ? "MCQ" : "FREE_TEXT"), Math.floor(i / 4) + 1]));
const quizAssignments = [];
for (let qz = 1; qz <= 25; qz++) for (let j = 0; j < 10; j++) quizAssignments.push([qz, ((qz * 3 + j) % teachers.length) + 1]);
rows("quiz_assignments", ["quiz_id", "teacher_id"], quizAssignments);
rows("quiz_submissions", ["id", "answers", "evaluation_text", "score", "submitted_at", "training_suggestion", "quiz_id", "teacher_id"], quizAssignments.slice(0, 180).map((a, i) => [i + 1, q('{"1":"B","2":"Analyse complete","3":"C","4":"Synthese"}'), q("Evaluation satisfaisante avec axes d'amelioration identifies."), 8 + (i % 13), dt(-40 + (i % 35)), q("Suivre le module de consolidation et refaire une activite d'application."), a[0], a[1]]));

rows("conversations", ["id", "last_message_time", "user1_id", "user2_id"], Array.from({ length: 45 }, (_, i) => [i + 1, dt(-20 + (i % 20)), inspectors[i % inspectors.length].id, teachers[(i * 2) % teachers.length].id]));
rows("messages", ["id", "content", "is_read", "timestamp", "conversation_id", "sender_id"], Array.from({ length: 180 }, (_, i) => {
  const c = (i % 45) + 1;
  const sender = i % 2 === 0 ? inspectors[(c - 1) % inspectors.length].id : teachers[((c - 1) * 2) % teachers.length].id;
  return [i + 1, q(pick(["Bonjour, merci de confirmer votre disponibilite.", "Le rapport est disponible pour consultation.", "Pouvez-vous partager la progression annuelle ?", "Bien recu, je prepare les documents."], i)), i % 3 === 0 ? 0 : 1, dt(-18 + (i % 18)), c, sender];
}));
rows("notifications", ["id", "created_at", "is_read", "message", "target_url", "title", "type", "recipient_id"], Array.from({ length: 220 }, (_, i) => [i + 1, dt(-30 + (i % 30)), i % 4 === 0 ? 0 : 1, q(pick(["Nouvelle activite planifiee.", "Rapport finalise.", "Quiz assigne.", "Message recu.", "Formation publiee."], i)), q(pick(["/calendar", "/reports", "/quizzes", "/messages", "/courses"], i)), q(pick(["Activite", "Rapport", "Quiz", "Message", "Formation"], i)), q(pick(["ACTIVITY", "REPORT", "QUIZ", "MESSAGE", "COURSE"], i)), (i % 100) + 1]));
rows("action_logs", ["id", "action_type", "created_at", "description", "entity_id", "entity_type", "ip_address", "user_id"], Array.from({ length: 260 }, (_, i) => [i + 1, q(pick(["LOGIN", "CREATE", "UPDATE", "EXPORT"], i)), dt(-45 + (i % 45)), q(`Operation ${i + 1} effectuee dans l'environnement de demonstration.`), q(String((i % 120) + 1)), q(pick(["User", "Activity", "Report", "Quiz", "Course"], i)), q(`192.168.1.${(i % 200) + 10}`), (i % 100) + 1]));
rows("timetable_slots", ["id", "classroom", "day_of_week", "end_time", "level", "start_time", "subject", "teacher_profile_id"], Array.from({ length: 240 }, (_, i) => [i + 1, q(`Salle ${100 + (i % 40)}`), q(pick(["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"], i)), q(`${String(9 + (i % 6)).padStart(2, "0")}:55:00`), q(pick(["6eme", "7eme", "8eme", "9eme", "1ere", "2eme", "Bac"], i)), q(`${String(8 + (i % 6)).padStart(2, "0")}:00:00`), q(pick(subjects, i)), (i % teachers.length) + 1]));

fs.writeFileSync(out, sql.join("\n\n") + "\n", "utf8");
console.log(out);
