var imageControllers = angular.module('imageControllers', []);

imageControllers.controller('IconCtrl', ['$scope', '$http', '$log',
  function ($scope, $http, $log) {
    $scope.refreshImage('icon');
    $scope.refreshImage('subscript');
    angular.element('.cls-file-upload').fileupload({
      add: function (e, data) {
        data.submit();
      },
      done: function (e, data) {
        $scope.afterUpload(data.result);
        $scope.$apply();
      }
    });
  }]);

imageControllers.controller('WatermarkCtrl', ['$scope', '$http', '$log',
  function ($scope, $http, $log) {

  }]);
