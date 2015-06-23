var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('GlobalStatsController',
    function ($rootScope, $scope, GlobalStats) {

        $scope.loading_stats = true;
        GlobalStats.query().$promise.then(
            function (data) {
                $scope.loading_stats = false;
                $scope.stats = data;
            },
            function (error) {
                $scope.loading_stats = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

    }
);