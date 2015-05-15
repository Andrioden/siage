var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('AdminController',
    function ($rootScope, $scope, Admin, User, $timeout) {

        $scope.Recalc = function () {
            $scope.recalc_processing = true;
            $scope.recalc_response = "";
            $scope.recalc_error = "";
            Admin.recalc().$promise.then(
                //success
                function (data) {
                    $scope.recalc_response = data.response;
                    $scope.recalc_processing = false;
                    $timeout(function () {
                        $scope.recalc_response = "";
                    }, 5000);
                },
                //error
                function (error) {
                    $scope.recalc_processing = false;
                    $scope.recalc_error = $rootScope.getFriendlyErrorText(error);
                }
            );
        };

        $scope.CleanDB = function () {
            $scope.cleandb_processing = true;
            $scope.cleandb_response = "";
            $scope.cleandb_error = "";
            Admin.cleandb().$promise.then(
                //success
                function (data) {
                    $scope.cleandb_response = data.response;
                    $scope.cleandb_processing = false;
                    $timeout(function () {
                        $scope.cleandb_response = "";
                    }, 5000);
                },
                //error
                function (error) {
                    $scope.cleandb_processing = false;
                    $scope.cleandb_error = $rootScope.getFriendlyErrorText(error);
                }
            );
        };

        $scope.ClearStats = function () {
            $scope.clearstats_processing = true;
            $scope.clearstats_response = "";
            $scope.clearstats_error = "";
            Admin.clearstats().$promise.then(
                //success
                function (data) {
                    $scope.clearstats_response = data.response;
                    $scope.clearstats_processing = false;
                    $timeout(function () {
                        $scope.clearstats_response = "";
                    }, 5000);
                },
                //error
                function (error) {
                    $scope.clearstats_processing = false;
                    $scope.clearstats_error = $rootScope.getFriendlyErrorText(error);
                }
            );
        };
    }
);
