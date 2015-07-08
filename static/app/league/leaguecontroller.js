var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('LeagueController',
    function ($rootScope, $scope, Player, Game, $location) {

        $scope.loading_players = true;
        Player.query(
            function (data) {
                $scope.players = data;
                $scope.loading_players = false;
            }
            ,function(error){
                $scope.loading_players = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

        $scope.loading_games = true;
        Game.query({max: 10},
            function (data) {
                $scope.games = data;
                $scope.loading_games = false;
            }
            ,function(error){
                $scope.loading_games = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            });

        $scope.navigate = function (route) {
            $location.path(route);
        };
    });