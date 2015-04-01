var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('SetupGamesController',
    function ($scope, Player, SetupGame, $routeParams) {
        $scope.SetupGame = { 'players': [] };
        $scope.algorithms = ["Random", "Autobalance"];
        $scope.SetupGame.algorithm = "Autobalance";

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

        $scope.ToggleSelectAllPlayers = function () {
            var isSynced = true;
            for (i = 0; i < $scope.players.length; i++) {
                for (j = 0; j < $scope.players.length; j++) {
                    if ($scope.players[i].joining != $scope.players[j].joining) {
                        isSynced = false;
                    }
                }
            }

            if (!isSynced) {
                for (i = 0; i < $scope.players.length; i++) {
                    $scope.players[i].joining = true;
                }
            } else {
                for (i = 0; i < $scope.players.length; i++) {
                    $scope.players[i].joining = !$scope.players[i].joining;
                }
            }
        };

        $scope.setupGame = function () {
            if (!hasEnoughPlayers()) {
                $scope.error = "Select at least 3 players!";
                $scope.games = [];
                return;
            };

            $scope.settingUpGame = true;

            var trebVoteList = [];
            for (var i = 0; i < $scope.players.length; i++) {
                if ($scope.players[i].joining) {
                    $scope.SetupGame.players.push($scope.players[i].id);
                    if ($scope.players[i].trebuchet_vote) {
                        trebVoteList.push(true);
                    } else {
                        trebVoteList.push(false);
                    }
                };
            }

            rollTrebuchet(trebVoteList);

            SetupGame.submit($scope.SetupGame).$promise.then(
                //success
                function (data) {
                    $scope.error = "";
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

        function hasEnoughPlayers() {
            var count = 0;
            for (i = 0; i < $scope.players.length; i++) {
                if ($scope.players[i].joining) {
                    count++;
                };
            }

            if (count >= 3) return true;
            return false;
        }

        function randomIntFromInterval(min, max) {
            return Math.floor(Math.random() * (max - min + 1) + min);
        }

        function rollTrebuchet(trebVoteList) {
            var randomInt = randomIntFromInterval(0, trebVoteList.length-1);
            $scope.trebuchet_allowed = trebVoteList[randomInt];
            console.log("Rolling trebuchet. Not the same order as original list:");
            console.log("Index " + randomInt + " from (" + trebVoteList + ") resulting in: " + trebVoteList[randomInt]);
        }
    }
);