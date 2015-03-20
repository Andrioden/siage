var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('LeagueController',
    function ($scope, Player, Game, $location) {

        $scope.loading_players = true;
        Player.query(
            function (data) {
                for (var i = 0; i < data.length; i++) {
                    if (data[i].played > 0) {
                        data[i].win_percent = Math.round(data[i].wins * 100 / data[i].played);
                    } else data[i].win_percent = 0;
                };
                $scope.players = data;
                $scope.loading_players = false;
            }
            ,function(error){
                $scope.loading_players = false;
                $scope.error = "Unable to load league list!";
            });

        $scope.loading_games = true;
        Game.query(
            function (data) {
                $scope.games = data;
                $scope.loading_games = false;
            }
            ,function(error){
                $scope.loading_games = false;
                $scope.error = "Unable to load game list!";
            });

        $scope.navigate = function (route) {
            $location.path(route);
        };
    });