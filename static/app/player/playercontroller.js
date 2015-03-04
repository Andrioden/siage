var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('PlayerController',
    function ($scope, Player, $routeParams) {
        Player.get({player_id: $routeParams.playerId},
            function (data) {
                $scope.player = data;
            },
            function (error) {
                $scope.error = "Unable to load player info!";
            })
    });