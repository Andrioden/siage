var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('PlayerController',
    function ($rootScope, $scope, Player, User, Game, $routeParams) {
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

                drawRatingGraph(data);
            }
            , function (error) {
                $scope.loading_games = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            });
        };
    }
);


google.load('visualization', '1', { packages: ['corechart', 'line'] });

function drawRatingGraph(player_results) {
    var chartData = prepareChartData(player_results);

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'X');
    data.addColumn('number', 'Rating');

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
        legend: { position: 'none' }

    };

    var chart = new google.visualization.LineChart(document.getElementById('rating_graph'));
    chart.draw(data, options);
}

function prepareChartData(player_results) {
    var chartData = [];

    for (i = 0; i < player_results.length; i++) {
        var temp = [
            player_results[i].date,
            parseInt(player_results[i].stats_rating)
        ];

        chartData.push(temp);
    }

    chartData.reverse();

    return chartData;
}
