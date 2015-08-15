var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('SetupGamesController',
    function ($rootScope, $scope, Player, Rule, SetupGame, $routeParams) {
        $scope.SetupGame = { 'players': [] };
        $scope.algorithms = ["AutoBalance", "AutoBalanceSAMR", "Random", "RandomManyTeams",];
        $scope.SetupGame.algorithm = "AutoBalance";

        $scope.loading_players = true;
        Player.query(
            function (data) {
                $scope.players = data;
                $scope.loading_players = false;
            }
            , function (error) {
                $scope.loading_players = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

        Rule.query(
            function (data) {
                $scope.rules = data;
            }
            , function (error) {
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

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
            }
            else {
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
            var ruleChoiceList = [];
            $scope.SetupGame.players = [];
            for (var i = 0; i < $scope.players.length; i++) {
                if ($scope.players[i].joining) {
                    $scope.SetupGame.players.push({
                        'id': $scope.players[i].id,
                        'rating': $scope.players[i].rating
                    });
                    if ($scope.players[i].trebuchet_vote) {
                        trebVoteList.push(true);
                    } else {
                        trebVoteList.push(false);
                    }
                    ruleChoiceList.push($scope.players[i].rule_choice);
                };
            }

            rollTrebuchet(trebVoteList);
            rollRuleChoice(ruleChoiceList)

            SetupGame.submit($scope.SetupGame).$promise.then(
                //success
                function (data) {
                    $scope.error = "";
                    $scope.games = data.games;
                    $scope.total_rating_dif = data.total_rating_dif;
                    $scope.settingUpGame = false;
                },
                //error
                function (error) {
                    $scope.settingUpGame = false;
                    $scope.error = $rootScope.getFriendlyErrorText(error);
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

        function rollRuleChoice(ruleChoiceList) {
            console.log(ruleChoiceList)
            var randomInt = randomIntFromInterval(0, ruleChoiceList.length-1);
            $scope.rule_choice = ruleChoiceList[randomInt];
        }

    }
);