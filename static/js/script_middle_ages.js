var ctx = document.getElementById('medieval-chart').getContext('2d');
var chart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Православие', 'Ислам', 'Иудаизм', 'Католицизм', 'Язычество'],
        datasets: [{
            data: [40, 35, 15, 5, 5],  // Примерные проценты
            backgroundColor: [
                'rgba(75, 192, 192, 0.6)', 
                'rgba(153, 102, 255, 0.6)', 
                'rgba(255, 159, 64, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 99, 132, 0.6)'
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Религиозное распределение в Средневековом Крыму'
            },
            legend: {
                position: 'right'
            }
        }
    }
});

    
    ymaps.ready(init);

function init() {
var map = new ymaps.Map("yandex-map", {
    center: [44.952116, 34.102411], // Координаты Крыма
    zoom: 7
});

// Основные точки морских путей
var routes = [
    {
        name: "Генуэзский путь из Ростова в Кафу",
        points: [
            [47.146174, 39.229339],  
            [46.961067, 38.399186],  
            [46.811756, 37.848169],  
            [46.743257, 37.638258],
            [45.593148, 36.718721],
            [45.427024, 36.697115],  
            [45.365006, 36.668027],
            [45.201271, 36.484317],
            [45.088752, 36.479063],
            [45.022140, 36.397848],
            [44.979336, 35.851384],
            [45.034126, 35.392240],
            [45.029559, 35.391655]

        ]
    },
    {
        name: "Херсонес путь в Константинополь",
        points: [
            [44.608623, 33.483413],  
            [44.618029, 33.472293],  
            [44.590136, 33.345471],
            [41.242936, 29.154037],
            [41.188979, 29.092709], 
            [41.166031, 29.067326],
            [41.151215, 29.065565],
            [41.126869, 29.076655],
            [41.114231, 29.071178],
            [41.095257, 29.058502],  
            [41.082115, 29.059203],
            [41.073958, 29.051629],
            [41.065408, 29.049029],
            [41.048016, 29.035551],
            [41.042094, 29.026698],
            [41.031007, 29.003974],
            [41.029379, 29.002928],
            [41.019518, 29.002484], 
            [40.992422, 28.982952],
            [40.812520, 28.704974], 
            [40.725545, 27.491581],  
            [40.501772, 27.119562],
            [40.429831, 26.749857],
            [40.388273, 26.682281], 
            [40.218256, 26.463641],
            [40.197831, 26.373912],
            [40.146490, 26.391967],
            [40.119829, 26.372631],
            [40.028680, 26.260170],
            [40.039745, 25.602067],


            [40.192234, 25.241957],
            [39.776623, 24.029550],
            [39.630924, 23.537496],
            [39.314989, 23.535966],
            [39.202685, 23.378583],
            [39.088562, 23.334772],

            [39.054627, 23.082476],
            [39.080133, 23.014975],
            [39.340824, 22.967503],
            [39.351886, 22.946524],
            [39.350162, 22.939192],
            [39.355331, 22.938502],
            [39.358639, 22.937263],

        ]
    },
    {
        name: "Судак — Египет",
        points: [
            [44.838969, 34.961659],  
            [44.838575, 34.962927],  
            [44.815900, 34.961255],
            [43.322215, 34.548893],
            [41.292173, 29.239516],
            [41.242936, 29.154037],
            [41.188979, 29.092709], 
            [41.166031, 29.067326],
            [41.151215, 29.065565],
            [41.126869, 29.076655],
            [41.114231, 29.071178],
            [41.095257, 29.058502],  
            [41.082115, 29.059203],
            [41.073958, 29.051629],
            [41.065408, 29.049029],
            [41.048016, 29.035551],
            [41.042094, 29.026698],
            [41.031007, 29.003974],  
            [41.029379, 29.002928],
            [41.019518, 29.002484], 
            [41.000773, 28.995496],
            [40.770063, 28.860709],
            [40.744397, 27.622781], 
            [40.504952, 27.061050],
            [40.422442, 26.735353], 
            [40.305692, 26.597066],  
            [40.211258, 26.448776],   
            [40.201797, 26.386812],   
            [40.132103, 26.389700],   

            [40.031169, 26.242351],   
            [40.034402, 25.842222],   
            [38.767049, 25.129649],   

            [38.123726, 25.297883],   
            [37.273960, 25.934711],   
            [36.931676, 26.234112],

            [36.562033, 26.753516], 
            [35.896454, 27.434557],  
            [34.791977, 27.547764], 

            [31.162528, 29.822579],  
            [31.162222, 29.848553], 

            [31.178335, 29.850971],  
            [31.194858, 29.871000], 
            [31.194592, 29.878702], 

        ]
    },
    {
        name: "Херсонес путь в Константинополь",
        points: [
            [44.608623, 33.483413],  
            [44.618029, 33.472293],  
            [44.590136, 33.345471],
            [41.242936, 29.154037],
            [41.188979, 29.092709], 
            [41.166031, 29.067326],
            [41.151215, 29.065565],
            [41.126869, 29.076655],
            [41.114231, 29.071178],
            [41.095257, 29.058502],  
            [41.082115, 29.059203],
            [41.073958, 29.051629],
            [41.065408, 29.049029],
            [41.048016, 29.035551],
            [41.042094, 29.026698],
            [41.031007, 29.003974],
            [41.029379, 29.002928],
            [41.019518, 29.002484],
            [41.000773, 28.995496],
            [40.770063, 28.860709],

        ]
    },
    {
        name: "Херсонес – Синоп",
        points: [
        [44.598498, 33.470191],  
        [44.605330, 33.468872],  
        [44.609618, 33.471295],
        [44.622714, 33.469204],
        [44.614880, 33.337948],
        [43.795259, 33.140743],
        [42.077223, 35.313530],
        [42.005514, 35.214778],
        [42.011321, 35.142341],
        [42.023602, 35.141968],

        ]
    },
    {
        name: "Судак – Трапезунд",
        points: [
        [44.838969, 34.961659],  
        [44.838575, 34.962927],  
        [44.837486, 34.966509],
        [44.779222, 34.980187],
        [44.473165, 35.101265],
        [41.055076, 39.707576],
        [41.020665, 39.732572],
        [41.008587, 39.756492],
        [41.004944, 39.751676],
        [41.004434, 39.746958],
        [41.001349, 39.747478],

        ]
    },
    {
        name: "Керчь – Марсель",
        points: [
        [45.272933, 36.416583],  
        [45.275280, 36.421631],  
        [45.279606, 36.424107],
        [45.277322, 36.452263],
        [45.244678, 36.481591],
        [45.099322, 36.533856],
        [44.857501, 36.539714],
        [43.224043, 33.118910],
        [41.285343, 29.187899],
        [41.242936, 29.154037],
        [41.188979, 29.092709], 
        [41.166031, 29.067326],
        [41.151215, 29.065565],
        [41.126869, 29.076655],
        [41.114231, 29.071178],
        [41.095257, 29.058502],  
        [41.082115, 29.059203],
        [41.073958, 29.051629],
        [41.065408, 29.049029],
        [41.048016, 29.035551],
        [41.042094, 29.026698],
        [41.031007, 29.003974],
        [41.029379, 29.002928],
        [40.994835, 28.992120],
        [40.916839, 28.935697],  
        [40.759326, 27.575767],
        [40.705590, 27.403066],
        [40.520979, 27.164258],
        [40.436915, 26.751969],
        [40.372041, 26.661224],
        [40.213409, 26.453304],
        [40.199977, 26.380370],
        [40.130521, 26.390828],
        [40.096877, 26.336591],
        [40.026876, 26.234170],  
        [39.946351, 25.691526],
        [38.112544, 24.741396],
        [37.834340, 24.531724],
        [37.683867, 24.209349],
        [37.020617, 23.938167],  
        [36.800559, 24.033919],
        [36.049257, 23.271455],
        [35.418154, 21.190064],
        [36.335994, 14.498293],
        [37.801411, 11.194984],  
        [38.372750, 6.420197],
        [43.171705, 5.220020],
        [43.281331, 5.339802],
        [43.291616, 5.344299],
        [43.297078, 5.356341],  
        [43.299271, 5.359143],
        [43.312097, 5.363385],
        ]
    },
    {
        name: "Судак – Новороссийск",
        points: [
        [44.838969, 34.961659],  
        [44.838575, 34.962927],  
        [44.837486, 34.966509],
        [44.777194, 34.976561],

        [44.723994, 35.148276],
        [44.184301, 36.176144],
        [44.406289, 37.645341],
        [44.649261, 37.845503],
        [44.689291, 37.827312],
        [44.714470, 37.820487],
        [44.719020, 37.826535],
        [44.720322, 37.828769],

        ]
    },
    {
        name: "Феодосия – Сочи",
        points: [
            [45.029559, 35.391655],
            [45.034126, 35.392240],

            [45.024939, 35.537021],  
            [44.856966, 35.746763],  
            [44.307103, 36.496448],  
            [43.475408, 38.213985],
            [43.467218, 39.658860],
            [43.570903, 39.719420],  
            [43.578056, 39.717088],
            [43.577545, 39.714345],
            [43.581060, 39.714698],
            [43.582048, 39.717160],


        ]
    },
    {
        name: "Ялта – Анапа",
        points: [
            [44.493102, 34.166222],
            [44.491008, 34.166158],

            [44.489079, 34.168178],  
            [44.443068, 34.239939],  
            [44.401774, 34.636714],  
            [44.637937, 36.078938],
            [44.879987, 36.934350],
            [44.910809, 37.286369],  
            [44.902233, 37.304198],
            [44.900002, 37.305650],



        ]
    },
];

// Добавляем пути на карту
routes.forEach(function(route) {
    var seaRoute = new ymaps.Polyline(route.points, {
        balloonContent: route.name
    }, {
        strokeColor: "#0000FF",
        strokeWidth: 4,
        strokeOpacity: 0.6
    });

    map.geoObjects.add(seaRoute);
});
}
