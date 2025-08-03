// LÓGICA PARA LA INTERACTIVIDAD DEL DASHBOARD

// Obtener datos del gráfico de categorías
const obtenerOptionChart = async () => {
    try
    {
        const response = await fetch("http://localhost:8000/inventario/existencias_por_categoria/")
        return await response.json();
    }
    catch(ex)
    {
        alert(ex);
    }
}

// Iniciar gráfico de categorías
const iniciarGraficoCategorias = async () => {
    // Detectar si el modo oscuro está activo por clase "dark-mode"
    const esModoOscuro = document.body.classList.contains('dark-mode');

    const graficoCategorias = echarts.init(document.getElementById('GraficoCategorias'), esModoOscuro ? 'dark' : 'light');
    let data = await obtenerOptionChart();

    const option = {
        dataset: [
            {
                dimensions: ['name', 'score'],
                source: data.dataset
            },
            {
                transform: {
                    type: 'sort',
                    config: { dimension: 'score', order: 'desc' }
                }
            }
        ],
        yAxis: {
            type: 'category',
            axisLabel: {
                interval: 0,
                rotate: 0  // inclinación para nombres largos
            }
        },
        xAxis: {},
        series: {
            type: 'bar',
            encode: {
                x: 'score',
                y: 'name'
            },
            datasetIndex: 1,
            itemStyle: {
                color: '#4da6ff'
            },
            label: {
                show: true,
                position: 'right',  // 'top' si el gráfico es vertical
                formatter: '{@score}'
            }
        }
    };

    graficoCategorias.setOption(option);
    graficoCategorias.resize();
}


window.addEventListener("load", async () => {
    await iniciarGraficoCategorias();
})