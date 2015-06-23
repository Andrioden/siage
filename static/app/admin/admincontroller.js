var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('AdminController',
    function ($rootScope, $scope, Admin, Player, User, $timeout) {

        $scope.loading_unverified_players = true;

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

        $scope.VerifyClaim = function (player) {
            $scope.verifyplayer_processing = true;
            $scope.verifyplayer_response = "";
            $scope.verifyplayer_error = "";

            Player.update({ player_id: player.nick }, { verified: true}).$promise.then(
                //success
                function (data) {
                    $scope.verifyplayer_processing = false;
                    if(data.verified){
                        $scope.verifyplayer_response = "Player claim for " + data.nick + " verified";
                        removePlayerFromUnverifiedList(player);
                    }
                    else {
                        $scope.verifyplayer_error = "Failed to verify player claim for " + data.nick;
                    }
                },
                //error
                function (error) {
                    $scope.verifyplayer_processing = false;
                    $scope.verifyplayer_error = $rootScope.getFriendlyErrorText(error);
                }
              );
        };

        $scope.RejectClaim = function (player) {
            $scope.verifyplayer_processing = true;
            $scope.verifyplayer_response = "";
            $scope.verifyplayer_error = "";

            Player.update({ player_id: player.nick }, { userid: null }).$promise.then(
                //success
                function (data) {
                    $scope.verifyplayer_processing = false;
                    if (!data.claimed) {
                        $scope.verifyplayer_response = "Player claim for " + data.nick + " successfully rejected";
                        removePlayerFromUnverifiedList(player);
                    }
                    else {
                        $scope.verifyplayer_error = "Failed to reject player claim for " + data.nick;
                    }
                },
                //error
                function (error) {
                    $scope.verifyplayer_processing = false;
                    $scope.verifyplayer_error = $rootScope.getFriendlyErrorText(error);
                }
              );
        };

        $scope.Recalc = function () {
            $scope.recalc_processing = true;
            $scope.recalc_response = "";
            $scope.recalc_error = "";
            Admin.recalcrating().$promise.then(
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
        
        function removePlayerFromUnverifiedList(player) {
            for (var i=0; i<$scope.unverified_players.length; i++ ) {
                if ($scope.unverified_players[i].id == player.id) $scope.unverified_players.splice(i,1);
            }
        }

    }
);
