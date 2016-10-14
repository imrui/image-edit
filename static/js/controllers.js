var imageControllers = angular.module('imageControllers', []);

// var get_file_path = function (file_info) {
//   if (!file_info) {
//     return ''
//   }
//   var info = file_info.split('/');
//   if (info.length != 2) {
//     return ''
//   }
//   return info[0]
// };

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
        $scope.iconsPath = '';
        $scope.$apply();
      }
    });
    var refreshIcons = function () {
      // if ($scope.subscript) {
      //   $scope.iconsPath = get_file_path($scope.icon) + '-' + get_file_path($scope.subscript);
      // } else {
      //   $scope.iconsPath = get_file_path($scope.icon);
      // }
      $scope.iconsPath = $scope.getImgCookies('icons-' + $scope.info.os.id);
    };
    $scope.changeOsType = function () {
      if ($scope.appIconSet) {
        $scope.iconSet = $scope.appIconSet[$scope.info.os.id];
      }
      refreshIcons();
    };
    $scope.$on('on_finish_app_icon_set', function () {
      $scope.changeOsType();
    });
    $scope.changeOsType();
    // refreshIcons();
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
        $scope.setImgCookies('icons-' + param.os, data.fp);
        refreshIcons();
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
