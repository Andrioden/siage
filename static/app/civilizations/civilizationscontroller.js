var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('CivilizationsController',
    function ($rootScope, $scope, Civilization, $location) {

        $scope.loading_civilizations = true;
        Civilization.query(
            function (data) {
                $scope.civilizations = data;
                $scope.setBestAndWorstPlayersForCivs();
                $scope.loading_civilizations = false;
                $scope.error = "";
            }
            ,function(error){
                $scope.loading_civilizations = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            });

        $scope.navigate = function (route) {
            $location.path(route);
        };


        $scope.setBestAndWorstPlayersForCivs = function () {
            for (i = 0; i < $scope.civilizations.length; i++) {
                var player_fits = $scope.civilizations[i].stats.player_fit;
                player_fits.sort(comparePointsForPlayers);
                $scope.civilizations[i].stats.best_players = player_fits.slice(0, 3);
                $scope.civilizations[i].stats.worst_player = player_fits.slice(player_fits.length - 1, player_fits.length)[0];
            };
        };

        function comparePointsForPlayers(a, b) {
            if (a.points < b.points)
                return 1;
            if (a.points > b.points)
                return -1;
            return 0;
        }
    });