var imageControllers = angular.module('imageControllers', []);

imageControllers.controller('IconCtrl', ['$scope', '$log', 'IconMerge',
  function ($scope, $log, IconMerge) {
    $scope.osOptions = [
      {id: 'android', name: "Android"},
      {id: 'ios', name: "Ios"}
    ];
    $scope.info = {os: $scope.osOptions[0]};
    var osType = $scope.getImgCookies('osType');
    if (osType) {
      for (var i=0; i<$scope.osOptions.length; i++) {
        if ($scope.osOptions[i].id == osType) {
          $scope.info.os = $scope.osOptions[i];
          break;
        }
      }
    }
    $scope.refreshImage('icon');
    $scope.refreshImage('subscript');
    var clearIconsPath = function () {
        $scope.removeImgCookies('icons-' + $scope.osOptions[0].id);
        $scope.removeImgCookies('icons-' + $scope.osOptions[1].id);
        $scope.iconsPath = '';
    };
    angular.element('.cls-file-upload').fileupload({
      add: function (e, data) {
        data.submit();
      },
      done: function (e, data) {
        $scope.afterUpload(data.result);
        clearIconsPath();
        $scope.$apply();
      }
    });
    var refreshIcons = function () {
      $scope.iconsPath = $scope.getImgCookies('icons-' + $scope.info.os.id);
    };
    $scope.changeOsType = function () {
      if ($scope.appIconSet) {
        $scope.iconSet = $scope.appIconSet[$scope.info.os.id];
      }
      refreshIcons();
      $scope.setImgCookies('osType', $scope.info.os.id);
    };
    $scope.$on('on_finish_app_icon_set', function () {
      $scope.changeOsType();
    });
    $scope.changeOsType();
    // refreshIcons();
    $scope.delSubscript = function () {
      if (!$scope.subscript) {
        return;
      }
      $scope.subscript = '';
      $scope.removeImgCookies('subscript');
      clearIconsPath();
    };
    $scope.iconMerge = function () {
      if (!$scope.icon) {
        alert('请上传icon');
        return;
      }
      var param = {os: $scope.info.os.id, icon: $scope.icon};
      if ($scope.subscript) {
        param.subscript = $scope.subscript;
      }
      $log.debug(param);
      IconMerge.get(param, function (data) {
        $log.debug(data);
        if (data.code == 404) {
          clearIconsPath();
          $scope.icon = '';
          $scope.subscript = '';
          $scope.removeImgCookies('icon');
          $scope.removeImgCookies('subscript');
          alert('icon或角标已失效，请重新上传！');
          return;
        }
        if (data.code != 200) {
          alert(data.code + ': ' + data.msg);
          return;
        }
        $scope.setImgCookies('icons-' + param.os, data.fp);
        refreshIcons();
      });
    };
  }]);

imageControllers.controller('WatermarkCtrl', ['$scope', '$http', '$log',
  function ($scope, $http, $log) {

  }]);
