import React, { useState, useEffect, useCallback } from "react";
import { getSystemHealth, getMetricDetails } from "../api/admin";
import { Activity, Shield, HardDrive, Cpu, Zap, AlertCircle, CheckCircle2, RefreshCw } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function SystemHealthCard() {
  const { t } = useTranslation();
  const [health, setHealth] = useState(null);
  const [metrics, setMetrics] = useState({
    cpu: 0,
    memory: 0,
    uptime: 0
  });
  const [loading, setLoading] = useState(true);
  // "up" | "down" | "waking" — "waking" = 503 cold start
  const [serverState, setServerState] = useState("waking");
  const [retrying, setRetrying] = useState(false);

  const fetchData = useCallback(async (manual = false) => {
    if (manual) setRetrying(true);
    try {
      let healthData = null;
      try {
        const healthRes = await getSystemHealth();
        healthData = healthRes.data;
        setServerState(healthData?.status === "UP" ? "up" : "down");
      } catch (healthErr) {
        const status   = healthErr?.response?.status;
        const bodyData = healthErr?.response?.data;

        if (status === 503 && bodyData?.status) {
          // Spring Boot returned 503 because a health component (e.g. DB) is DOWN
          // The response body IS a valid health JSON — treat it as a real outage
          healthData = bodyData;
          setServerState("down");
        } else if (status === 503) {
          // No Spring Boot body → Render cold start, server not yet accepting connections
          setServerState("waking");
          setHealth({ status: "WAKING" });
          return; // Skip metric calls — server hasn't booted yet
        } else if (bodyData) {
          healthData = bodyData;
          setServerState("down");
        } else {
          // Network offline / CORS / total connection failure
          setServerState("waking");
          setHealth({ status: "WAKING" });
          return;
        }
      }
      setHealth(healthData || { status: "DOWN" });

      // Fetch metrics individually so one failure doesn't zero out the rest
      const safeMetric = async (name) => {
        try {
          const res = await getMetricDetails(name);
          return res.data.measurements[0].value;
        } catch {
          return null;
        }
      };

      const [cpuVal, memVal, uptimeVal] = await Promise.all([
        safeMetric("system.cpu.usage"),
        safeMetric("jvm.memory.used"),
        safeMetric("process.uptime"),
      ]);

      setMetrics({
        cpu:    cpuVal    != null ? (cpuVal    * 100).toFixed(1)          : null,
        memory: memVal    != null ? (memVal    / (1024 * 1024)).toFixed(0) : null,
        uptime: uptimeVal != null ? (uptimeVal / 3600).toFixed(1)          : null,
      });
    } finally {
      setLoading(false);
      setRetrying(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    // Poll every 60 s — no need to hammer a sleeping free-tier server
    const interval = setInterval(() => fetchData(), 60000);
    return () => clearInterval(interval);
  }, [fetchData]);

  if (loading) return null;

  const isUp    = serverState === "up";
  const isWaking = serverState === "waking";

  // ── Shared card shell ──────────────────────────────────────────────────────
  const cardStyle = {
    background: 'white',
    borderRadius: '20px',
    padding: '1.5rem',
    boxShadow: '0 4px 20px rgba(0,0,0,0.05)',
    border: `1px solid ${isWaking ? '#fde68a' : '#f1f5f9'}`,
    marginBottom: '2rem'
  };

  // Badge colour logic
  const badgeBg    = isUp ? '#dcfce7' : isWaking ? '#fef3c7' : '#fee2e2';
  const badgeColor = isUp ? '#15803d' : isWaking ? '#92400e' : '#b91c1c';
  const iconBg     = isUp ? '#dcfce7' : isWaking ? '#fef3c7' : '#fee2e2';
  const iconColor  = isUp ? '#15803d' : isWaking ? '#d97706' : '#ef4444';

  const metricBoxStyle = {
    background: '#f8fafc',
    borderRadius: '16px',
    padding: '1.25rem',
    border: '1px solid #f1f5f9',
    flex: 1
  };

  return (
    <div style={cardStyle}>
      {/* ── Header ── */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ background: iconBg, color: iconColor, padding: '10px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Shield size={20} />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 800, color: '#1e293b' }}>System Health Monitor</h3>
            <p style={{ margin: 0, fontSize: '0.8rem', color: '#94a3b8', fontWeight: 600 }}>Real-time backend telemetry</p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* Manual retry button */}
          <button
            onClick={() => fetchData(true)}
            disabled={retrying}
            title="Retry now"
            style={{
              background: 'none', border: '1px solid #e2e8f0', borderRadius: '10px',
              padding: '5px 10px', cursor: retrying ? 'not-allowed' : 'pointer',
              display: 'flex', alignItems: 'center', gap: '5px',
              color: '#64748b', fontSize: '0.75rem', fontWeight: 700,
              opacity: retrying ? 0.5 : 1, transition: 'opacity 0.2s'
            }}
          >
            <RefreshCw size={13} style={{ animation: retrying ? 'spin 1s linear infinite' : 'none' }} />
            {retrying ? 'Checking…' : 'Retry'}
          </button>

          {/* Status badge */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '6px 14px', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 800, background: badgeBg, color: badgeColor }}>
            {isUp    ? <CheckCircle2 size={14} /> : <AlertCircle size={14} />}
            {isUp ? 'OPERATIONAL' : isWaking ? 'WAKING UP' : 'ISSUES DETECTED'}
          </div>
        </div>
      </div>

      {/* ── Cold-start / waking state ── */}
      {isWaking ? (
        <div style={{
          background: '#fffbeb', border: '1px dashed #fcd34d', borderRadius: '16px',
          padding: '1.5rem', textAlign: 'center'
        }}>
          <p style={{ margin: '0 0 4px', fontWeight: 800, color: '#92400e', fontSize: '0.95rem' }}>
            ⏳ Backend server is waking up (Render free tier)
          </p>
          <p style={{ margin: 0, color: '#b45309', fontSize: '0.8rem' }}>
            The service spins down after 15 min of inactivity. It will be ready in ~30–60 s.
            The page will auto-refresh every 60 seconds, or click <strong>Retry</strong> above.
          </p>
        </div>
      ) : (
        /* ── Metric boxes (only shown when server is reachable) ── */
        <div style={{ display: 'flex', gap: '1.25rem', flexWrap: 'wrap' }}>
          {/* CPU */}
          <div style={metricBoxStyle}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#64748b', marginBottom: '0.75rem' }}>
              <Cpu size={16} />
              <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>CPU Usage</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800, color: metrics.cpu != null ? '#1e293b' : '#94a3b8' }}>
                {metrics.cpu != null ? `${metrics.cpu}%` : 'N/A'}
              </span>
              {metrics.cpu != null && <span style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 600 }}>LOAD</span>}
            </div>
            <div style={{ marginTop: '1rem', width: '100%', background: '#e2e8f0', borderRadius: '10px', height: '6px', overflow: 'hidden' }}>
              <div style={{ width: `${metrics.cpu != null ? Math.min(metrics.cpu * 2, 100) : 0}%`, background: '#4f46e1', height: '100%', borderRadius: '10px', transition: 'width 0.5s ease' }} />
            </div>
          </div>

          {/* MEMORY */}
          <div style={metricBoxStyle}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#64748b', marginBottom: '0.75rem' }}>
              <HardDrive size={16} />
              <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>JVM Memory</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800, color: metrics.memory != null ? '#1e293b' : '#94a3b8' }}>
                {metrics.memory != null ? metrics.memory : 'N/A'}
              </span>
              {metrics.memory != null && <span style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 600 }}>MB USED</span>}
            </div>
            <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Activity size={12} color="#6366f1" />
              <span style={{ fontSize: '0.7rem', color: '#6366f1', fontWeight: 700, letterSpacing: '0.05em' }}>LIVE FEED</span>
            </div>
          </div>

          {/* UPTIME */}
          <div style={metricBoxStyle}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#64748b', marginBottom: '0.75rem' }}>
              <Zap size={16} />
              <span style={{ fontSize: '0.85rem', fontWeight: 700 }}>System Uptime</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800, color: metrics.uptime != null ? '#1e293b' : '#94a3b8' }}>
                {metrics.uptime != null ? metrics.uptime : 'N/A'}
              </span>
              {metrics.uptime != null && <span style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: 600 }}>HOURS</span>}
            </div>
            <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <div style={{ width: '8px', height: '8px', background: metrics.uptime != null ? '#22c55e' : '#cbd5e1', borderRadius: '50%', boxShadow: metrics.uptime != null ? '0 0 8px #22c55e' : 'none' }} />
              <span style={{ fontSize: '0.7rem', color: metrics.uptime != null ? '#15803d' : '#94a3b8', fontWeight: 700 }}>
                {metrics.uptime != null ? 'STABLE' : 'UNAVAILABLE'}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Spinner keyframe (inline) */}
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
