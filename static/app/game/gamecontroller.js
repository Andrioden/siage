var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('GameController', $routeParams,
    function ($scope, Game) {
        Game.get($routeParams.gameId,
            function (data) {
                $scope.game = data;
            },
            function (error) {
                $scope.gameInfoError = "Unable to load player info!";
            })
    });

