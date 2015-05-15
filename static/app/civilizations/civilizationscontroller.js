var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('CivilizationsController',
    function ($rootScope, $scope, Civilization, $location) {

        $scope.loading_civilizations = true;
        Civilization.query(
            function (data) {
                $scope.civilizations = data;
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
    });