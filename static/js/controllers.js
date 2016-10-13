var imageControllers = angular.module('imageControllers', []);

imageControllers.controller('IconCtrl', ['$scope', '$log', 'IconMerge',
  function ($scope, $log, IconMerge) {
    $scope.osOptions = [
      {id: 'android', name: "Android"},
      {id: 'ios', name: "Ios"}
    ];
    $scope.info = {os: $scope.osOptions[0]};
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
    $scope.changeOsType = function () {
      $scope.iconSet = $scope.appIconSet[$scope.info.os.id];
    };
    $scope.changeOsType();
    $scope.iconMerge = function () {
      var param = {os: $scope.info.os.id, icon: $scope.icon};
      if ($scope.subscript) {
        param.subscript = $scope.subscript;
      }
      $log.debug(param);
      IconMerge.get(param, function (data) {
        $log.debug(data);
      });
    };
    $scope.iconDownload = function () {
      $log.debug($scope.icon);
      $log.debug($scope.subscript);
    };
  }]);

imageControllers.controller('WatermarkCtrl', ['$scope', '$http', '$log',
  function ($scope, $http, $log) {

  }]);
