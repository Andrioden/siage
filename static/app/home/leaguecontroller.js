var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('LeagueController',
    function ($scope, Player, $location) {
        Player.query(
            function (data) {
            $scope.players = data;}
            ,function(error){
             $scope.error = "Unable to load league list!";
            });
        
        $scope.navigate = function (route) {
            $location.path(route);
        }
    });