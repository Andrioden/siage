var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('LeagueController',
    function ($scope, Players) {
        Players.query(
            function (data) {
            $scope.players = data;}
            ,function(error){
             $scope.playerListError = "Unable to load player list!";
            });
    });