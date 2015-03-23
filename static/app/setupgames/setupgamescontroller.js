var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('SetupGamesController',
    function ($scope, Player, SetupGame, $routeParams) {
        $scope.SetupGame = { 'players': [] };
        $scope.algorithms = ["Random", "Best random"];
        $scope.SetupGame.algorithm = "Best random";

        $scope.loading_players = true;
        Player.query(
            function (data) {
                for (var i = 0; i < data.length; i++) {
                    data[i].win_percent = Math.round(data[i].wins * 100 / data[i].played);
                };
                $scope.players = data;
                $scope.loading_players = false;
            }
            , function (error) {
                $scope.loading_players = false;
                $scope.error = "Unable to load league list!";
            });

        $scope.setupGame = function () {
            $scope.settingUpGame = true;
            for (var i = 0; i < $scope.players.length; i++) {
                if ($scope.players[i].joining) {
                    $scope.SetupGame.players.push($scope.players[i].id);
                };
            }

            SetupGame.submit($scope.SetupGame).$promise.then(
                //success
                function (data) {
                    $scope.games = data.games;
                    $scope.total_rating_dif = data.total_rating_dif;
                    $scope.SetupGame.players = [];
                    $scope.settingUpGame = false;
                },
                //error
                function (error) {
                    $scope.settingUpGame = false;
                    $scope.error = "Unable to setup game!";
                }
            );
        };
    }
);