﻿var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('PlayerController',
    function ($rootScope, $scope, Player, User, Game, Rule, PlayerAction, $routeParams, $location, $timeout) {
        $scope.user = User.get();

        $scope.loading_player = true;
        Player.get({ player_id: $routeParams.playerId },
            function (data) {
                $scope.loading_player = false;
                $scope.player = data;
                loadGames(data.id);
            },
            function (error) {
                $scope.loading_player = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
    	);

        Rule.query(
            function (data) {
                $scope.rules = data;
            }
            , function (error) {
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

        $scope.updateSettingTrebuchet = function() {
            $scope.player_setting_trebuchet_response = "";
            update({setting_default_trebuchet_allowed: $scope.player.settings.default_trebuchet_allowed}, 'player_setting_trebuchet_response');
        }

        $scope.updateSettingRule = function() {
            $scope.player_setting_rule_response = "";
            update({setting_default_rule_id: $scope.player.settings.default_rule}, 'player_setting_rule_response');
        }

        $scope.navigate = function (route) {
            $location.path(route);
        };

        // PRIVATE METHODS

        function loadGames(playerId) {
            Game.query({ player_id: playerId },
                function (data) {
                    $scope.games = data;
                    $scope.loading_games = false;
                    var rating_offset = $scope.player.rating_adjustment + $scope.player.rating_decay;
                    drawRatingGraph(data, rating_offset);
                }
                , function (error) {
                    $scope.loading_games = false;
                    $scope.error = $rootScope.getFriendlyErrorText(error);
                }
            );
        }

        function update(data, scopeResponseVariable) {
            Player.update({ player_id: $scope.player.nick }, data).$promise.then(
                //success
                function (data) {
                    $scope[scopeResponseVariable] = "Updated setting";
                    $timeout(function () {
                        $scope[scopeResponseVariable] = "";
                    }, 5000);
                },
                //error
                function (error) {
                    $scope.error = $rootScope.getFriendlyErrorText(error);
                }
            );
        }

    }
);

google.load('visualization', '1', { packages: ['corechart', 'line'] });

function drawRatingGraph(player_results, rating_offset) {
    var chartData = prepareChartData(player_results, rating_offset);
    var lowestValue = getLowestRatingValue(chartData);

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
            baseline: lowestValue - 10,
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
            easing: 'linear',
            startup: true
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

function prepareChartData(player_results, rating_offset) {
    var chartData = [];

    for (i = 0; i < player_results.length; i++) {
        var temp = [
            new Date(player_results[i].date_epoch * 1000).ddmmyyyy(),
            parseInt(player_results[i].stats_rating),
            '/games/' + player_results[i].id
        ];

        chartData.push(temp);
    }

    chartData.push(['Joined', 1000 + rating_offset, '']);
    chartData.reverse();

    return chartData;
}

function getLowestRatingValue(chartData) {
    var lowestValue = chartData[0][1];

    for (i = 0; i < chartData.length; i++) {
        if(chartData[i][1] < lowestValue){
            lowestValue = chartData[i][1]
        }
    }

    return lowestValue;
}