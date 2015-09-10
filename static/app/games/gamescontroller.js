var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('GamesController',
    function ($rootScope, $scope, Game, $routeParams) {
        $scope.gameSearchQuery = { 'searchString': "" };
        $scope.loading_games = true;
        Game.query({ data_detail: 'full' },
            function (data) {
                $scope.games = data;
                $scope.generateSearchStrings();
                $scope.loading_games = false;
                $scope.error = "";
            }
            , function (error) {
                $scope.loading_games = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            });

        $scope.getPlayersFromGame = function (game)
        {
            var result = "";
            var first = true;
            game.player_results.sort(compareTeams);
            game.player_results.forEach(function (playerResult) {
                if (!first) {
                    result += ",";
                }
                result += " " + playerResult.player.nick;
                if (playerResult.is_winner) {
                    result += "(W)";
                } else {
                    result += "(L)";
                }
                first = false;
            });
            return result;
        }

        function compareTeams(a, b) {
            if (a.team < b.team)
                return -1;
            if (a.team > b.team)
                return 1;
            return 0;
        }

        $scope.generateSearchStrings = function() {
            for (i = 0; i < $scope.games.length; i++) {
                var game = $scope.games[i];
                var date = new Date(0);
                date.setUTCSeconds($scope.games[i].date_epoch);
                $scope.games[i].date = date.toLocaleDateString();
                game.searchString = date.toLocaleDateString() + " | " + game.title + " " + game.team_format;
                game.searchString += " | " + $scope.getPlayersFromGame(game);
                if (game.trebuchet_allowed) {
                    game.searchString += " | TrebOn";
                } else {
                    game.searchString += " | TrebOff";
                }
            }
        };

        $scope.matchEveryWord = function () {
            return function (item) {
                var string = JSON.stringify(item).toLowerCase();
                var words = $scope.gameSearchQuery.searchString.toLowerCase();

                if (words) {
                    var filterBy = words.split(/\s+/);
                    if (!filterBy.length) {
                        return true;
                    }
                } else {
                    return true;
                }

                return filterBy.every(function (word) {

                    var exists = string.indexOf(word);
                    if (exists !== -1) {
                        return true;
                    }
                });
            };
        };
    }
);