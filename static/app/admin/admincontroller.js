var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('AdminController',
    function ($rootScope, $scope, AdminAction, Player, User, $timeout) {

        $scope.loading_players = true;

        Player.query(
            function (data) {
                $scope.players = data;
                $scope.loading_players = false;
            }
            ,function(error){
                $scope.error = $rootScope.getFriendlyErrorText(error);
                $scope.loading_players = false;
            }
        );

        $scope.loading_unverified_players = true;
        $scope.adjust_rating_values = {};

        Player.query({ verified: false, claimed: true }).$promise.then(
            function (data) {
                $scope.unverified_players = data;
                $scope.loading_unverified_players = false;
                $scope.error = "";
            },
            function (error) {
                $scope.loading_unverified_players = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

        $scope.Recalc = function () {
            $scope.recalc_processing = true;
            $scope.recalc_response = "";
            $scope.recalc_error = "";
            AdminAction.recalcrating().$promise.then(
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

        $scope.FixDB = function () {
            $scope.fixdb_processing = true;
            $scope.fixdb_response = "";
            $scope.fixdb_error = "";
            AdminAction.fixdb().$promise.then(
                //success
                function (data) {
                    $scope.fixdb_response = data.response;
                    $scope.fixdb_processing = false;
                    $timeout(function () {
                        $scope.fixdb_response = "";
                    }, 5000);
                },
                //error
                function (error) {
                    $scope.fixdb_processing = false;
                    $scope.fixdb_error = $rootScope.getFriendlyErrorText(error);
                }
            );
        };

        $scope.ClearStats = function () {
            $scope.clearstats_processing = true;
            $scope.clearstats_response = "";
            $scope.clearstats_error = "";
            AdminAction.clearstats().$promise.then(
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

        $scope.AdjustRating = function () {
            $scope.adjustrating_processing = true;
            $scope.adjustrating_response = "";
            $scope.adjustrating_error = "";
            AdminAction.adjustrating($scope.adjust_rating_values).$promise.then(
                //success
                function (data) {
                    $scope.adjustrating_response = data.response;
                    $scope.adjustrating_processing = false;
                    $timeout(function () {
                        $scope.adjustrating_response = "";
                    }, 5000);
                },
                //error
                function (error) {
                    $scope.adjustrating_processing = false;
                    $scope.adjustrating_error = $rootScope.getFriendlyErrorText(error);
                }
            );
        }

        $scope.setPlayerRatingAdjustment = function() {
            console.log($scope.adjust_rating_values);
            for (var i=0; i<$scope.players.length; i++ ) {
                if ($scope.players[i].id == $scope.adjust_rating_values.player_id)
                    $scope.adjust_rating_values.new_rating_adjustment = $scope.players[i].rating_adjustment;
            }
        }

        $scope.ResetRatingAdjustment = function () {
            $scope.resetratingadjustment_processing = true;
            $scope.resetratingadjustment_response = "";
            $scope.resetratingadjustment_error = "";
            AdminAction.resetratingadjustment().$promise.then(
                //success
                function (data) {
                    $scope.resetratingadjustment_response = data.response;
                    $scope.resetratingadjustment_processing = false;
                    $timeout(function () {
                        $scope.resetratingadjustment_response = "";
                    }, 5000);
                },
                //error
                function (error) {
                    $scope.resetratingadjustment_processing = false;
                    $scope.resetratingadjustment_error = $rootScope.getFriendlyErrorText(error);
                }
            );
        }

        $scope.setPlayerActiveState = function(player, state) {
            updatePlayer(player, {active: state});
        }

        $scope.verifyClaim = function (player) {
            updatePlayer(player, {verified: true});
        };

        $scope.rejectClaim = function (player) {
            updatePlayer(player, {userid: null, claimed: false});
        };

        $scope.updating_player_processing = false;

        function updatePlayer(player, updateValues) {
            $scope.updating_player_processing = true;
            Player.update({ player_id: player.nick }, updateValues).$promise.then(
                //success
                function (data) {
                    angular.extend(player, updateValues);
                    $scope.updating_player_processing = false;
                },
                //error
                function (error) {
                    $scope.updating_player_error = $rootScope.getFriendlyErrorText(error);
                    $scope.updating_player_processing = false;
                }
            );
        }
        
        function removePlayerFromUnverifiedList(player) {
            for (var i=0; i<$scope.unverified_players.length; i++ ) {
                if ($scope.unverified_players[i].id == player.id) $scope.unverified_players.splice(i,1);
            }
        }

    }
);
