var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterGameController',
    function ($scope, GameSetting, Player, Game, $timeout) {
        initGame();
        GameSetting.query().$promise.then(
            function (value) {
                $scope.error = "";
                $scope.game_types = value.game_types;
                $scope.locations = value.locations;
                $scope.sizes = value.sizes;
                $scope.resources_list = value.resources;
                $scope.game_speeds = value.game_speeds;
                $scope.victory_list = value.victories;
                $scope.teams = value.teams;
                $scope.civilizations = value.civilizations;
                $scope.starting_ages = value.starting_ages;
                $scope.treaty_lengths = value.treaty_lengths;
                $scope.populations = value.populations;
                $scope.difficulties = value.difficulties;
                $scope.reveal_map = value.reveal_map;
            },
            function (error) {
                $scope.error = "Unable to load settings";
            }
        );

        Player.query().$promise.then(
            function (value) {
                emptyPlayerHelper = [{'player_id': "", 'first': true}];
                $scope.allPlayers = emptyPlayerHelper.concat(value);
            },
            function (value) {
                $scope.error = "Unable to load players";
            }
        );

        $scope.submitting = false;
        $scope.submitGame = function () {
            if(!confirmWinner()){
                $scope.error = "Select a winner!";
                return;
            }
            cleanPlayerResults();
            $scope.submitting = true;
            $scope.game.duration_seconds = $scope.game.duration_minutes * 60;
            $scope.game.date_epoch = Math.round($scope.game.date.getTime() / 1000);
            Game.save($scope.game).$promise.then(
                //success
                function (value) {
                    initGame();
                    resetAllPlayers();
                    $scope.error = "";
                    $scope.success = value.response;
                    $scope.submitted_game_id = value.game_id;
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
                    $scope.submitted_game_id = "";
                    reAddEmptyPlayers();
                    $scope.submitting = false;
                }
            );

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
            if (playerResult.player_id != "") {
                if (playerResult.is_winner && playerResult.team != null) {
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
                else if (playerResult.is_winner && playerResult.team == null) {
                    for (j = 0; j < $scope.game.playerResults.length; j++) {
                        if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                            $scope.game.playerResults[j].is_winner = false;
                        }
                    }
                }

                else if (playerResult.is_winner == false && playerResult.team != null) {
                    for (j = 0; j < $scope.game.playerResults.length; j++) {
                        if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                            if (playerResult.team == $scope.game.playerResults[j].team) {
                                $scope.game.playerResults[j].is_winner = false;
                            }
                        }
                    }
                }
            }
            for (j = 0; j < $scope.game.playerResults.length; j++) {
                if ($scope.game.playerResults[j].player_id == "") {
                    $scope.game.playerResults[j].is_winner = false;
                }
            }
        };


        $scope.setWinnersByTeamChange = function (playerResult) {
            if (playerResult.player_id != "") {
                if (playerResult.is_winner == false && playerResult.team != null) {
                    for (j = 0; j < $scope.game.playerResults.length; j++) {
                        if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                            if (playerResult.team == $scope.game.playerResults[j].team) {
                                playerResult.is_winner = $scope.game.playerResults[j].is_winner;
                            }
                        }
                    }
                }else if (playerResult.is_winner && playerResult.team != null) {
                    for (j = 0; j < $scope.game.playerResults.length; j++) {
                        if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                            if (playerResult.team == $scope.game.playerResults[j].team) {
                                $scope.game.playerResults[j].is_winner = playerResult.is_winner;
                            }else{
                                $scope.game.playerResults[j].is_winner =!playerResult.is_winner;
                            }
                        }
                    }
                }
                else if (playerResult.is_winner && playerResult.team == null) {
                    for (j = 0; j < $scope.game.playerResults.length; j++) {
                        if (playerResult.player_id != $scope.game.playerResults[j].player_id) {
                            $scope.game.playerResults[j].is_winner = false;
                        }
                    }
                }
            }
            for (j = 0; j < $scope.game.playerResults.length; j++) {
                if ($scope.game.playerResults[j].player_id == "") {
                    $scope.game.playerResults[j].is_winner = false;
                }
            }
        };

        function initGame() {
            $scope.game = new Game();
            $scope.game.date = new Date();
            $scope.game.duration_seconds = null;
            $scope.game.game_type = null;
            $scope.game.location = null;
            $scope.game.size = null;
            $scope.game.difficulty = null;
            $scope.game.resources = null;
            $scope.game.game_speed = null;
            $scope.game.reveal_map = null
            $scope.game.victory = null;
            $scope.game.starting_age = null;
            $scope.game.treaty_length = null;
            $scope.game.population = null;
            $scope.game.all_techs = false;
            $scope.game.team_together = false;
            $scope.game.trebuchet_allowed = false;
            $scope.game.playerResults = [];
            for (i = 0; i < 8; i++) {
                $scope.game.playerResults.push({
                    'player_id': "",
                    'civilization': null,
                    'team': null,
                    'score': null,
                    'is_winner': false
                });
            }
        };

        function reAddEmptyPlayers() {
            while ($scope.game.playerResults.length < 8) {
                $scope.game.playerResults.push({
                    'player_id': "",
                    'civilization': null,
                    'team': null,
                    'score': null,
                    'is_winner': false
                });
            }
        };

        function resetAllPlayers() {
            for (j = 0; j < $scope.allPlayers.length; j++) {
                $scope.allPlayers[j].isinuse = false;
            }
        };

        function confirmWinner(){
            var winner_found = false;
            for (i = 0; i < $scope.game.playerResults.length; i++) {
                if($scope.game.playerResults[i].is_winner){ winner_found = true; }
            }
            return winner_found;
        }
    })
;

