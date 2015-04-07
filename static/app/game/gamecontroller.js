var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('GameController',
    function ($rootScope, $scope, Game, $routeParams) {
        $scope.loading_game = true;
        Game.get({ game_id: $routeParams.gameId, data_detail: 'full' },
            function (data) {
                $scope.loading_game = false;
                $scope.game = data;
                $scope.game.duration_minutes = data.duration_seconds/60;
            },
            function (error) {
                $scope.loading_game = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );
    }
);