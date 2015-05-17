var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('PlayerController',
    function ($rootScope, $scope, Player, User, Game, $routeParams) {
        $scope.user = User.get();

        $scope.loading_player = true;
        Player.get({ player_id: $routeParams.playerId },
            function (data) {
                $scope.loading_player = false;
                $scope.player = data;

                $scope.load_games_for_player();
            },
            function (error) {
                $scope.loading_player = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
    	);

        $scope.load_games_for_player = function () {
            Game.query({ player_id: $scope.player.id },
            function (data) {
                $scope.games = data;
                $scope.loading_games = false;
            }
            , function (error) {
                $scope.loading_games = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            });
        };
    }
);