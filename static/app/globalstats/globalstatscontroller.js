var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('GlobalStatsController',
    function ($rootScope, $scope, GlobalStats) {

        $scope.loading_stats = true;

        $scope.activity = null;
        $scope.loading_activity = false;

        GlobalStats.base().$promise.then(
            function (data) {
                $scope.loading_stats = false;
                $scope.stats = data;
            },
            function (error) {
                $scope.loading_stats = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );


        // PUBLIC METHODS

        $scope.loadActivity = function() {
            $scope.loading_activity = true;

            GlobalStats.activity().$promise.then(
                function (data) {
                    $scope.loading_activity = false;
                    $scope.activity = data;
                    drawActivityGraph();
                },
                function (error) {
                    $scope.loading_activity = false;
                    $scope.error = $rootScope.getFriendlyErrorText(error);
                }
            );
        }


        // PRIVATE METHODS

        function drawActivityGraph() {
            google.load('visualization', '1', { packages: ['corechart', 'line'] });

            var chartData = prepareChartData($scope.activity);

            var data = new google.visualization.DataTable();
            data.addColumn('date', 'Date');
            data.addColumn('number', 'Players');

            data.addRows(chartData);

            var options = {
                hAxis: {
                    title: '',
                    gridlines: {
                        color: 'transparent'
                    }
                },
                vAxis: {
                    title: 'Players',
                    gridlines: {
                        color: 'transparent'
                    }
                },
                backgroundColor: { fill: 'transparent' },
                colors: ['#df633b'],
                pointSize: 5,
                legend: { position: 'none' },
            };

            var chart = new google.visualization.LineChart(document.getElementById('activity_graph'));
            chart.draw(data, options);
        }

        function prepareChartData(activity) {
            var chartData = [];

            for (var i = 0; i < activity.length; i++) {
                chartData.push([new Date(activity[i].date_epoch * 1000), activity[i].player_count])
            }

            return chartData;
        }
    }
);