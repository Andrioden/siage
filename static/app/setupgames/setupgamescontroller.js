var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('SetupGamesController',
    function ($rootScope, $scope, Player, Rule, PlayerAction, $routeParams, $timeout, GameSetting) {
        $scope.SetupGame = {
            'players': [],
            'max_game_rating_dif': 9999,
            'attempts': 500,
            'map_style_weight': {
                'megarandom': 30,
                'random_land_map': 10,
                'the_unknown': 10,
                'any': 50
            },
            'roll_game_type': false
        };
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

        GameSetting.query().$promise.then(
            function (value) {
                $scope.error = "";
                $scope.game_types = value.game_types;
                $scope.locations = value.locations;
                $scope.rules = value.rules;
            },
            function (error) {
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
            rollRuleChoice(ruleChoiceList);
            rollMapStyle($scope.SetupGame.map_style_weight);
            rollGameType();

            $scope.games = undefined;
            $scope.total_rating_dif = undefined;

            PlayerAction.setupGame($scope.SetupGame).$promise.then(
                //success
                function (data) {
                    $scope.error = "";
                    $scope.games = data.games;
                    $scope.total_rating_dif = data.total_rating_dif;
                    $scope.settingUpGame = false;
                    $scope.registerGameUrls = buildRegisterGameUrls();
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

        function randomFromArray(arr) {
            var min = 0;
            var max = arr.length-1;
            var choice = Math.floor(Math.random() * (max - min + 1) + min);
            return arr[choice];
        }

        function rollTrebuchet(trebVoteList) {
            $scope.trebuchet_allowed = randomFromArray(trebVoteList)
        }

        function rollRuleChoice(ruleChoiceList) {
            $scope.rule_choice_id = randomFromArray(ruleChoiceList);
            if ($scope.rule_choice_id == null)
                $scope.rule_choice = "No Rule";
            else
                $scope.rule_choice = getRuleNameById($scope.rule_choice_id);
        }

        function rollMapStyle(weights) {
            // Build map style bucket to random from based on weights
            var mapStyleBucket = [];
            for (var mapType in weights){
                var weight = weights[mapType];
                for (var i = 0; i < weight; i++) mapStyleBucket.push(mapType)
            }
            // ROLL
            var mapStyleChoice = randomFromArray(mapStyleBucket);
            if (mapStyleChoice == "megarandom") $scope.map_style_choice = "MegaRandom";
            else if (mapStyleChoice == "random_land_map") $scope.map_style_choice = "Random Land map";
            else if (mapStyleChoice == "the_unknown") $scope.map_style_choice = "es@the_unknown_v2 ";
            else if (mapStyleChoice == "any") $scope.map_style_choice = randomFromArray($scope.locations);
        }

        function rollGameType() {
            if($scope.SetupGame.roll_game_type)
                $scope.game_type_choice = randomFromArray($scope.game_types);
            else
                $scope.game_type_choice = "";
        }

        function getRuleNameById(ruleId) {
            for (var i = 0; i < $scope.rules.length; i++) {
                if ($scope.rules[i].id == ruleId) return $scope.rules[i].name;
            }
            return "RuleNotFound: " + ruleId;
        }

        function buildRegisterGameUrls() {
            var urls = []
            for (var i = 0; i < $scope.games.length; i++) {
                urls.push(
                    "/registergame"
                    + "?treb=" + $scope.trebuchet_allowed
                    + "&rule=" + $scope.rule_choice_id
                    + "&map=" + $scope.map_style_choice
                    + "&type=" + $scope.game_type_choice
                    + buildPlayersGameUrl($scope.games[i])
                );
            }
            return urls;
        }

        function buildPlayersGameUrl(game) {
            var playersParams = "";
            var playerCounter = 0;
            for (var t = 0; t < game.teams.length; t++) {
                for (var p = 0; p < game.teams[t].players.length; p++) {
                    playerCounter++;
                    playersParams += "&player" + (playerCounter) + "=" + game.teams[t].players[p].id + "-" + game.teams[t].players[p].civ + "-" + (t+1);
                }
            }
            return playersParams;
        }

        function scrollToBottomOfPage() {
            window.scrollTo(0,document.body.scrollHeight);
        }

    }
);