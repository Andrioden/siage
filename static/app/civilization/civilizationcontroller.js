var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('CivilizationController',
    function ($rootScope, $scope, Civilization, $location, $routeParams) {

        $scope.loading_civilization = true;
        Civilization.get({ name: $routeParams.name },
            function (data) {
                $scope.civ = data;
                $scope.loading_civilization = false;
                $scope.error = "";
            }
            ,function(error){
                $scope.loading_civilization = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            });

        $scope.navigate = function (route) {
            $location.path(route);
        };
    });