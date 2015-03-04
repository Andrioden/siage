﻿var siAgeApp = angular.module('SiAgeApp');

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
                emptyPlayerHelper = [{'player_id': "", 'first': true}];
                $scope.allPlayers = emptyPlayerHelper.concat(value);
            },
            function (value) {
                $scope.error = "Unable to load players";
            }
        )

        $scope.submitting = false;
        $scope.submitGame = function () {
            cleanPlayerResults();
            $scope.submitting = true;
            Game.save($scope.game).$promise.then(
                //success
                function (value) {
                    initGame();
                    resetAllPlayers();
                    $scope.error = "";
                    $scope.success = value.response;
                    $scope.submitting = false;
                    $timeout(function () {
                        $scope.success = "";
                    }, 5000);

                },
                //error
                function (error) {
                    var result = "";
                    if (error.data) result = error.data;
                    else result = error.statusText;
                    $scope.error = "Save game failed: " + result;
                    reAddEmptyPlayers();
                    $scope.submitting = false;
                }
            )

            function cleanPlayerResults() {
                for (i = 0; i < $scope.game.playerResults.length; i++) {
                    if ($scope.game.playerResults[i].player_id == "") {
                        $scope.game.playerResults.splice(i, 1);
                        i--;
                    }
                }
            }
        };

        $scope.removeSelectedPlayersFromList = function () {
            resetAllPlayers();
            for (i = 0; i < $scope.game.playerResults.length; i++) {
                for (j = 0; j < $scope.allPlayers.length; j++) {
                    if ($scope.game.playerResults[i].player_id == $scope.allPlayers[j].id) {
                        $scope.allPlayers[j].isinuse = true;
                    }
                }
            }
        };

        $scope.setWinnersByWinToggle = function (playerResult) {
            console.log(playerResult);
            if (playerResult.is_winner & playerResult.team != 0) {
                for (j = 0; j < $scope.game.playerResults.length; j++) {
                    if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                        if (playerResult.team == $scope.game.playerResults[j].team) {
                            $scope.game.playerResults[j].is_winner = true;
                        } else {
                            $scope.game.playerResults[j].is_winner = false;
                        }
                    }
                }
            }
            else if (playerResult.is_winner & playerResult.team == 0) {
                for (j = 0; j < $scope.game.playerResults.length; j++) {
                    if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                        $scope.game.playerResults[j].is_winner = false;
                    }
                }
            }

            else if (playerResult.is_winner == false & playerResult.team != 0) {
                for (j = 0; j < $scope.game.playerResults.length; j++) {
                    if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                        if (playerResult.team == $scope.game.playerResults[j].team) {
                            $scope.game.playerResults[j].is_winner = false;
                        }
                    }
                }
            }
        }

        $scope.setWinnersByTeamChange = function (playerResult) {
            if (playerResult.team != 0) {
                for (j = 0; j < $scope.game.playerResults.length; j++) {
                    if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                        if (playerResult.team == $scope.game.playerResults[j].team) {
                            playerResult.is_winner = $scope.game.playerResults[j].is_winner;
                        }
                    }
                }
            } else if (playerResult.is_winner & playerResult.team == 0) {
                for (j = 0; j < $scope.game.playerResults.length; j++) {
                    if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                        $scope.game.playerResults[j].is_winner = false;
                    }
                }
            }
        }

        function initGame() {
            $scope.game = new Game();
            $scope.game.playerResults = [];
            for (i = 0; i < 8; i++) {
                $scope.game.playerResults.push({
                    'player_id': "",
                    'civilization': "",
                    'team': 0,
                    'score': "",
                    'is_winner': false
                });
            }
        };

        function reAddEmptyPlayers() {
            while ($scope.game.playerResults.length < 8) {
                $scope.game.playerResults.push({
                    'player_id': "",
                    'civilization': "",
                    'team': 0,
                    'score': "",
                    'is_winner': false
                });
            }
        };

        function resetAllPlayers() {
            for (j = 0; j < $scope.allPlayers.length; j++) {
                $scope.allPlayers[j].isinuse = false;
            }
        };
    });

