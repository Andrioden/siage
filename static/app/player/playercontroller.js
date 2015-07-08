var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('PlayerController',
    function ($rootScope, $scope, Player, User, Game, $routeParams, $location) {
        $scope.user = User.get();

        $scope.loading_player = true;
        Player.get({ player_id: $routeParams.playerId },
            function (data) {
                $scope.loading_player = false;
                $scope.player = data;
                $scope.load_games_for_player();
            },
            function (error) {
                $scope.loading_player = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
    	);

        $scope.load_games_for_player = function () {
            Game.query({ player_id: $scope.player.id },
            function (data) {
                $scope.games = data;
                $scope.loading_games = false;
                drawRatingGraph(data, $scope.player.rating_adjustment);
            }
            , function (error) {
                $scope.loading_games = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            });
        };

        $scope.navigate = function (route) {
            $location.path(route);
        };
    }
);


google.load('visualization', '1', { packages: ['corechart', 'line'] });

function drawRatingGraph(player_results, rating_adjustment) {
    var chartData = prepareChartData(player_results, rating_adjustment);

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Date');
    data.addColumn('number', 'Rating');
    data.addColumn({ type: 'string', name: 'URL', role: 'url' });

    data.addRows(chartData);

    var options = {
        hAxis: {
            title: '',
            logScale: false,
            textPosition: 'none'
        },
        vAxis: {
            title: '',
            logScale: false,
            textPosition: 'none',
            baselineColor: 'none',
            gridlines: {
                color: 'transparent'
            }

        },
        backgroundColor: { fill: 'transparent' },
        colors: ['#df633b'],
        pointSize: 5,
        chartArea: { 'width': '100%', 'height': '100%' },
        legend: { position: 'none' },
        animation: {
            duration: 1000,
            startup: 'true'
        }

    };

    var chart = new google.visualization.LineChart(document.getElementById('rating_graph'));
    chart.draw(data, options);

    var handler = function (e) {
        var sel = chart.getSelection();
        sel = sel[0];
        if (sel && sel['row'] && sel['column']) {
            var gameUrl = chartData[sel['row']][2];
            angular.element(document.getElementById('main_content')).scope().navigate(gameUrl);
            angular.element(document.getElementById('main_content')).scope().$apply();
        }
    }
    google.visualization.events.addListener(chart, 'select', handler);
}

function prepareChartData(player_results, rating_adjustment) {
    var chartData = [];

    for (i = 0; i < player_results.length; i++) {
        var temp = [
            player_results[i].date,
            parseInt(player_results[i].stats_rating),
            '/games/' + player_results[i].id
        ];

        chartData.push(temp);
    }

    chartData.push(['Joined', 1000 + rating_adjustment, '']);
    chartData.reverse();

    return chartData;
}
