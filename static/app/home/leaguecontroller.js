var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('LeagueController',
    function ($scope, Players) {
        $scope.players = Players.query();
    });