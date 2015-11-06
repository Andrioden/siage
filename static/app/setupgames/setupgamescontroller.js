var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('SetupGamesController',
    function ($rootScope, $scope, Player, Rule, PlayerAction, $routeParams, $timeout) {
        $scope.SetupGame = { 'players': [] };
        $scope.algorithms = ["AutoBalance", "AutoBalanceSAMR", "Random", "RandomManyTeams",];
        $scope.SetupGame.algorithm = "AutoBalanceSAMR";

        $scope.loading_players = true;
        Player.query({active: true},
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
                    trebVoteList.push($scope.players[i].settings.default_trebuchet_allowed);
                    ruleChoiceList.push($scope.players[i].settings.default_rule);
                };
            }

            rollTrebuchet(trebVoteList);
            rollRuleChoice(ruleChoiceList)

            PlayerAction.setupGame($scope.SetupGame).$promise.then(
                //success
                function (data) {
                    $scope.error = "";
                    $scope.games = data.games;
                    $scope.total_rating_dif = data.total_rating_dif;
                    $scope.settingUpGame = false;
                    // Scroll down, but give angularjs some time to draw the new games at the bottom.
                    $timeout(function () {
                        scrollToBottomOfPage();
                    }, 200);

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
            for (var i = 0; i < $scope.players.length; i++) {
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
            var ruleChoiceId = ruleChoiceList[randomInt];
            if (ruleChoiceId == null) $scope.rule_choice = "No Rule";
            else $scope.rule_choice = getRuleNameById(ruleChoiceId);
        }

        function getRuleNameById(ruleId) {
            for (var i = 0; i < $scope.rules.length; i++) {
                if ($scope.rules[i].id == ruleId) return $scope.rules[i].name;
            }
            return "RuleNotFound: " + ruleId;
        }

        function scrollToBottomOfPage() {
            window.scrollTo(0,document.body.scrollHeight);
        }

    }
);