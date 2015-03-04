var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterGameController',
    function ($scope, GameSetting, Player, Game, $timeout) {
        initGame();
        GameSetting.query().$promise.then(
            function (value) {
                $scope.error = "";
                $scope.game_types = value.game_types;
                $scope.map_types = value.map_type;
                $scope.map_sizes = value.map_size;
                $scope.resources_list = value.resources;
                $scope.gameSpeeds = [];
                $scope.victoryList = [];
                $scope.teams = value.teams;
                $scope.civilizations = value.civilizations;
                $scope.starting_ages = value.starting_age;
                $scope.populations = value.population;
            },
            function (error) {
                $scope.error = "Unable to load settings";
            }
        )

        Player.query().$promise.then(
            function (value) {
                $scope.allPlayers = value;
            },
            function (value) {
                $scope.error = "Unable to load players";
            }
        )


        $scope.submitGame = function () {
            cleanPlayerResults();
            Game.save($scope.game).$promise.then(
                //success
                function (value) {
                    initGame();
                    $scope.error = "";
                    $scope.success = value.response;
                    $timeout(function () {
                        $scope.success = "";
                    }, 5000);

                },
                //error
                function (error) {
                    $scope.error = error.data;
                }
            )

            function cleanPlayerResults() {
                for (i = 0; i < $scope.game.playerResults.length; i++) {
                    if ($scope.game.playerResults[i].player_id == "") {
                        $scope.game.playerResults.splice(i, 1);
                        i--;
                    }
                    ;
                }
            }
        };

        function initGame() {
            $scope.game = new Game();
            $scope.game.playerResults = [];
            for (i = 0; i < 8; i++) {
                $scope.game.playerResults.push({ 'player_id': "", 'civilization': "", 'team': 0, 'score': "", 'is_winner': false });
            }
        };
    });