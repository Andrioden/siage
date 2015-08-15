var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterRuleController',
    function ($rootScope, $scope, Rule, $timeout) {
        $scope.newrule = new Rule();
        $scope.rules = [];

        $scope.loading_rules = true;
        Rule.query(
            function (data) {
                $scope.loading_rules = false;
                $scope.rules = data;
                $scope.error = "";
            }
            , function (error) {
                $scope.loading_rules = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

        $scope.submitRule = function () {
            Rule.save($scope.newrule).$promise.then(
                //success
                function(rule_from_db) {
                    $scope.rules.push(rule_from_db);
                    $scope.newrule = new Rule();
                    $scope.error = "";
                    $timeout(function() {
                        $scope.success = "";
                    }, 5000);
                },
                //error
                function(error) {
                    $scope.error = $rootScope.getFriendlyErrorText(error);
                }
            );
        };

        $scope.deleteRule = function (rule_id) {
            Rule.delete({ rule_id: rule_id }).$promise.then(
                //success
                function(value) {
                    for(var i=0; i<$scope.rules.length; i++) {
                        if ($scope.rules[i].id == rule_id) $scope.rules.splice(i,1);
                    }
                    $scope.error = "";
                    $scope.success = value.response;
                    $timeout(function() {
                        $scope.success = "";
                    }, 5000);
                },
                //error
                function(error) {
                    $scope.error = $rootScope.getFriendlyErrorText(error);
                }
            );
        };
    }
);