﻿var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('GameController',
    function ($rootScope, $scope, Game, $routeParams) {
        $scope.loading_game = true;
        Game.get({ game_id: $routeParams.gameId, data_detail: 'full' },
            function (data) {
                $scope.loading_game = false;
                $scope.game = data;
                $scope.error = "";
            },
            function (error) {
                $scope.loading_game = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );
    }
);