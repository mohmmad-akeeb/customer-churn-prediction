/**
 * eda.js -  ChurnSight EDA Dashboard
 *
 * Fetches pre-computed statistics from /eda/data and renders
 * interactive Chart.js visualisations.
 */
(function () {
  'use strict';

  // ── Design tokens (match main.css CSS vars) ──────────────────
  const C = {
    indigo:    '#6366f1',
    indigoMid: '#818cf8',
    indigoLt:  '#c7d2fe',
    red:       '#dc2626',
    redLt:     '#fca5a5',
    green:     '#16a34a',
    greenLt:   '#86efac',
    amber:     '#d97706',
    amberLt:   '#fcd34d',
    gray200:   '#e2e8f0',
    gray400:   '#94a3b8',
    gray700:   '#334155',
    white:     '#ffffff',
  };

  const PALETTE = [
    C.indigo, C.red, C.green, C.amber,
    '#0ea5e9', '#8b5cf6', '#f97316', '#14b8a6',
  ];

  // ── Shared Chart.js defaults ─────────────────────────────────
  Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
  Chart.defaults.font.size   = 12;
  Chart.defaults.color       = C.gray400;
  Chart.defaults.plugins.legend.display = false;
  Chart.defaults.plugins.tooltip.backgroundColor = C.gray700;
  Chart.defaults.plugins.tooltip.padding         = 10;
  Chart.defaults.plugins.tooltip.cornerRadius    = 8;
  Chart.defaults.plugins.tooltip.titleFont       = { weight: '600', size: 12 };

  // ── Helpers ──────────────────────────────────────────────────
  function pct(v) { return v.toFixed(1) + '%'; }

  function barConfig(labels, data, colors, xLabel, yLabel) {
    return {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          data,
          backgroundColor: Array.isArray(colors) ? colors : labels.map(() => colors),
          borderRadius: 6,
          borderSkipped: false,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: { label: ctx => ' ' + ctx.parsed.y.toFixed(1) + (yLabel === '%' ? '%' : '') },
          },
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { maxRotation: 30 },
          },
          y: {
            grid: { color: C.gray200 },
            ticks: { callback: v => v + (yLabel === '%' ? '%' : '') },
            title: yLabel ? { display: true, text: yLabel, color: C.gray400 } : {},
          },
        },
      },
    };
  }

  // ── Populate KPI cards ───────────────────────────────────────
  function renderKPIs(d) {
    const ov = d.churn_overview;
    document.getElementById('kpiTotal').textContent    = ov.total_customers.toLocaleString();
    document.getElementById('kpiChurned').textContent  = ov.churned.toLocaleString();
    document.getElementById('kpiRetained').textContent = ov.retained.toLocaleString();
    document.getElementById('kpiRate').textContent     = ov.churn_rate_pct + '%';
  }

  // ── 1. Churn donut ───────────────────────────────────────────
  function renderChurnDonut(d) {
    const ov = d.churn_overview;
    new Chart(document.getElementById('churnDonut'), {
      type: 'doughnut',
      data: {
        labels: ['Retained', 'Churned'],
        datasets: [{
          data: [ov.retained, ov.churned],
          backgroundColor: [C.green, C.red],
          borderWidth: 0,
          hoverOffset: 8,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '68%',
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
            labels: { padding: 16, usePointStyle: true, pointStyleWidth: 10 },
          },
          tooltip: {
            callbacks: {
              label: ctx => ' ' + ctx.label + ': ' + ctx.parsed.toLocaleString()
                + ' (' + ((ctx.parsed / ov.total_customers) * 100).toFixed(1) + '%)',
            },
          },
        },
      },
    });
  }

  // ── 2. Contract bar ──────────────────────────────────────────
  function renderContractBar(d) {
    const cd = d.churn_by_contract;
    new Chart(
      document.getElementById('contractBar'),
      barConfig(cd.labels, cd.churn_pct,
        [C.red, C.amber, C.green], null, '%')
    );
  }

  // ── 3. Internet type bar ─────────────────────────────────────
  function renderInternetBar(d) {
    const id = d.churn_by_internet;
    new Chart(
      document.getElementById('internetBar'),
      barConfig(id.labels, id.churn_pct,
        [C.red, C.amber, C.indigoMid, C.green], null, '%')
    );
  }

  // ── 4. Tenure stacked ────────────────────────────────────────
  function renderTenureStacked(d) {
    const td = d.tenure_distribution;
    const retainedCounts = td.total_counts.map((t, i) => t - td.churn_counts[i]);
    new Chart(document.getElementById('tenureStacked'), {
      type: 'bar',
      data: {
        labels: td.bins,
        datasets: [
          {
            label: 'Retained',
            data: retainedCounts,
            backgroundColor: C.green,
            borderRadius: { topLeft: 0, topRight: 0 },
            borderSkipped: false,
          },
          {
            label: 'Churned',
            data: td.churn_counts,
            backgroundColor: C.red,
            borderRadius: { topLeft: 6, topRight: 6 },
            borderSkipped: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: { usePointStyle: true, pointStyleWidth: 10 },
          },
          tooltip: { mode: 'index', intersect: false },
        },
        scales: {
          x: { stacked: true, grid: { display: false } },
          y: {
            stacked: true,
            grid: { color: C.gray200 },
            title: { display: true, text: 'Customers', color: C.gray400 },
          },
        },
      },
    });
  }

  // ── 5. Monthly charge bar ────────────────────────────────────
  function renderChargeBar(d) {
    const mc = d.monthly_charge_bands;
    new Chart(
      document.getElementById('chargeBar'),
      barConfig(mc.labels, mc.churn_pct,
        mc.churn_pct.map(v => v > 35 ? C.red : v > 20 ? C.amber : C.green),
        null, '%')
    );
  }

  // ── 6. Payment method bar ────────────────────────────────────
  function renderPaymentBar(d) {
    const pm = d.churn_by_payment;
    new Chart(
      document.getElementById('paymentBar'),
      barConfig(pm.labels, pm.churn_pct,
        [C.red, C.amber, C.green, C.green], null, '%')
    );
  }

  // ── 7. Feature importance horizontal bar ────────────────────
  function renderFeatureImportance(d) {
    const fi = d.feature_importance;
    const reversed = {
      features:   [...fi.features].reverse(),
      importance: [...fi.importance].reverse(),
    };
    new Chart(document.getElementById('featureImportance'), {
      type: 'bar',
      data: {
        labels: reversed.features,
        datasets: [{
          data: reversed.importance,
          backgroundColor: reversed.importance.map((v, i) =>
            i >= reversed.importance.length - 2 ? C.indigo : C.indigoLt
          ),
          borderRadius: 4,
          borderSkipped: false,
        }],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          tooltip: {
            callbacks: { label: ctx => ' Importance: ' + (ctx.parsed.x * 100).toFixed(1) + '%' },
          },
        },
        scales: {
          x: {
            grid: { color: C.gray200 },
            ticks: { callback: v => (v * 100).toFixed(0) + '%' },
            title: { display: true, text: 'Gini Importance', color: C.gray400 },
          },
          y: { grid: { display: false } },
        },
      },
    });
  }

  // ── 8. Model comparison grouped bar ─────────────────────────
  function renderModelComparison(d) {
    const mc = d.model_comparison;
    new Chart(document.getElementById('modelComparison'), {
      type: 'bar',
      data: {
        labels: mc.models,
        datasets: [
          {
            label: 'Accuracy',
            data: mc.accuracy,
            backgroundColor: C.indigo,
            borderRadius: 4,
          },
          {
            label: 'ROC-AUC',
            data: mc.roc_auc,
            backgroundColor: C.green,
            borderRadius: 4,
          },
          {
            label: 'F1 (Churn)',
            data: mc.f1_churn,
            backgroundColor: C.amber,
            borderRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: { usePointStyle: true, pointStyleWidth: 10 },
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: { label: ctx => ' ' + ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(3) },
          },
        },
        scales: {
          x: { grid: { display: false } },
          y: {
            grid: { color: C.gray200 },
            min: 0.5,
            max: 1.0,
            ticks: { callback: v => v.toFixed(2) },
          },
        },
      },
    });
  }

  // ── 9. Offer churn bar ───────────────────────────────────────
  function renderOfferBar(d) {
    const oc = d.offer_churn;
    new Chart(
      document.getElementById('offerBar'),
      barConfig(oc.labels, oc.churn_pct,
        oc.churn_pct.map(v => v > 30 ? C.red : v > 10 ? C.amber : C.green),
        null, '%')
    );
  }

  // ── 10. Segment bar ──────────────────────────────────────────
  function renderSegmentBar(d) {
    const sg = d.senior_under30;
    new Chart(
      document.getElementById('segmentBar'),
      barConfig(sg.groups, sg.churn_pct,
        [C.red, C.green, C.indigoMid], null, '%')
    );
  }

  // ── Boot: fetch data then render all charts ──────────────────
  async function boot() {
    let data;
    try {
      const res = await fetch('/eda/data');
      if (!res.ok) throw new Error('HTTP ' + res.status);
      data = await res.json();
    } catch (err) {
      console.error('Failed to load EDA data:', err);
      return;
    }

    renderKPIs(data);
    renderChurnDonut(data);
    renderContractBar(data);
    renderInternetBar(data);
    renderTenureStacked(data);
    renderChargeBar(data);
    renderPaymentBar(data);
    renderFeatureImportance(data);
    renderModelComparison(data);
    renderOfferBar(data);
    renderSegmentBar(data);
  }

  boot();
})();
