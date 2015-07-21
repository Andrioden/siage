var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('LeagueController',
    function ($rootScope, $scope, Player, Game, $location) {

        $scope.full_players_data_loaded = false;
        $scope.show_full_players_data = false;

        $scope.loading_players = true;
        Player.query(
            function (data) {
                $scope.players = data;
                $scope.loading_players = false;
            }
            ,function(error){
                $scope.loading_players = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

        $scope.loading_games = true;
        Game.query({max: 10},
            function (data) {
                $scope.games = data;
                $scope.loading_games = false;
            }
            ,function(error){
                $scope.loading_games = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

        $scope.navigate = function (route) {
            $location.path(route);
        };

        $scope.toggleFullPlayersData = function () {
            if (!$scope.show_full_players_data) {
                if (!$scope.full_players_data_loaded) loadFullPlayersData();
                else $scope.show_full_players_data = true;
            }
            else $scope.show_full_players_data = false;
        }

        function loadFullPlayersData() {
            $scope.loading_players = true;
            Player.query({ data_detail: 'full' },
                function (data) {
                    $scope.players = data;
                    setBestPlayerFits();
                    $scope.loading_players = false;
                    $scope.full_players_data_loaded = true;
                    $scope.show_full_players_data = true;
                }
                ,function(error){
                    $scope.loading_players = false;
                    $scope.error = $rootScope.getFriendlyErrorText(error);
                }
            );
        }

        function setBestPlayerFits() {
            for (var i=0; i<$scope.players.length; i++) {
                var player = $scope.players[i];
                if (player.stats) {
                    sortFitListByPointsAndWinChance(player.stats.teammate_fit);
                    if(player.stats.teammate_fit[0]) player.stats.top_teammate_fit = player.stats.teammate_fit[0].teammate.nick;

                    sortFitListByPointsAndWinChance(player.stats.enemy_fit);
                    if(player.stats.enemy_fit[0]) player.stats.top_enemy_fit = player.stats.enemy_fit[0].enemy.nick;

                    sortFitListByPointsAndWinChance(player.stats.civ_fit);
                    if(player.stats.civ_fit[0]) player.stats.top_civ_fit = player.stats.civ_fit[0].civ;
                }
            }
        }

        // Uses the thenBy micro js library for sorting easier with multiple sort conditions
        function sortFitListByPointsAndWinChance(fitList) {
            fitList.sort(
                firstBy(function (v1, v2) { return v1.points - v2.points; }, -1)
                .thenBy(function (v1, v2) { return v1.win_chance - v2.win_chance; }, -1)
                .thenBy(function (v1, v2) { return v1.wins - v2.wins; }, -1)
                .thenBy(function (v1, v2) { return v1.score_per_min - v2.score_per_min; }, -1)
            )
        }

    }
);