   document.addEventListener("DOMContentLoaded", function() {
        
        // Configuración global de Chart.js para que se vea moderno
        Chart.defaults.global.defaultFontFamily = "'Roboto', 'Helvetica Neue', 'Helvetica', 'Arial', sans-serif";
        Chart.defaults.global.defaultFontColor = '#858796';

        // --- 1. Gráfico de Rangos (Barras) ---
        try {
            const rangosLabels = JSON.parse('{{ chart_rangos_labels|safe }}');
            const rangosCounts = JSON.parse('{{ chart_rangos_counts|safe }}');

            const ctxRango = document.getElementById('graficoVoluntariosPorRango').getContext('2d');
            new Chart(ctxRango, {
                type: 'bar',
                data: {
                    labels: rangosLabels,
                    datasets: [{
                        label: 'Voluntarios',
                        data: rangosCounts,
                        backgroundColor: '#D72600', /* Rojo Corporativo */
                        hoverBackgroundColor: '#b01f00',
                        borderColor: '#D72600',
                        borderWidth: 1,
                        borderRadius: 5, /* Bordes redondeados en barras (Chart.js v3+) */
                        barPercentage: 0.6,
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    layout: { padding: { left: 10, right: 25, top: 25, bottom: 0 } },
                    scales: {
                        xAxes: [{
                            gridLines: { display: false, drawBorder: false },
                            ticks: { maxTicksLimit: 6 },
                            maxBarThickness: 25,
                        }],
                        yAxes: [{
                            ticks: { min: 0, maxTicksLimit: 5, padding: 10 },
                            gridLines: { color: "rgb(234, 236, 244)", zeroLineColor: "rgb(234, 236, 244)", drawBorder: false, borderDash: [2], zeroLineBorderDash: [2] }
                        }],
                    },
                    legend: { display: false },
                    tooltips: {
                        backgroundColor: "rgb(255,255,255)",
                        bodyFontColor: "#858796",
                        titleMarginBottom: 10,
                        titleFontColor: '#6e707e',
                        titleFontSize: 14,
                        borderColor: '#dddfeb',
                        borderWidth: 1,
                        xPadding: 15,
                        yPadding: 15,
                        displayColors: false,
                        intersect: false,
                        mode: 'index',
                        caretPadding: 10,
                    }
                }
            });
        } catch (e) { console.error("Error gráfico rangos:", e); }

        // --- 2. Gráfico de Profesiones (Doughnut) ---
        try {
            const profesLabels = JSON.parse('{{ chart_profes_labels|safe }}');
            const profesCounts = JSON.parse('{{ chart_profes_counts|safe }}');
            
            const ctxProfesion = document.getElementById('graficoVoluntariosPorProfesion').getContext('2d');
            new Chart(ctxProfesion, {
                type: 'doughnut',
                data: {
                    labels: profesLabels,
                    datasets: [{
                        data: profesCounts,
                        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'],
                        hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf', '#dda20a', '#c0392b'],
                        hoverBorderColor: "rgba(234, 236, 244, 1)",
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    tooltips: {
                        backgroundColor: "rgb(255,255,255)",
                        bodyFontColor: "#858796",
                        borderColor: '#dddfeb',
                        borderWidth: 1,
                        xPadding: 15,
                        yPadding: 15,
                        displayColors: false,
                        caretPadding: 10,
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: { padding: 20, usePointStyle: true }
                    },
                    cutoutPercentage: 75,
                },
            });
        } catch (e) { console.error("Error gráfico profesiones:", e); }
    });