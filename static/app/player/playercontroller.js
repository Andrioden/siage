var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('PlayerController',
    function ($scope, Player, User, $routeParams) {
        $scope.loading_player = true;
        Player.get({player_id: $routeParams.playerId},
            function (data) {
                $scope.loading_player = false;
                $scope.player = data;
            },
            function (error) {
                $scope.loading_player = false;
                $scope.error = "Unable to load player info!";
            }
    	);

        $scope.user = User;
    }
);