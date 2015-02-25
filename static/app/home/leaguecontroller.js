var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('LeagueController',
    function ($scope, Player) {
        Player.query(
            function (data) {
            $scope.players = data;}
            ,function(error){
             $scope.playerListError = "Unable to load league list!";
            });
    });