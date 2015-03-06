var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('LeagueController',
    function ($scope, Player, Game, $location) {
        Player.query(
            function (data) {
            $scope.players = data;}
            ,function(error){
             $scope.error = "Unable to load league list!";
            });

        Game.query(
            function (data) {
                $scope.games = data;}
            ,function(error){
                $scope.error = "Unable to load game list!";
            });
        
        $scope.navigate = function (route) {
            $location.path(route);
        };
    });