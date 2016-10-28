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

imageControllers.controller('WatermarkCtrl', ['$scope', '$log', 'Watermark',
  function ($scope, $log, Watermark) {
    $scope.wmtOptions = [
      {id: 'txt', name: '文字水印'},
      {id: 'img', name: '图片水印'}
    ];
    $scope.wmpOptions = [
      {id: 'rb', name: '右下'},
      {id: 'lb', name: '左下'},
      {id: 'lt', name: '左上'},
      {id: 'rt', name: '右上'},
      {id: 'md', name: '中心'}
    ];
    $scope.fontsOptions = [
      {id: 'Open-Sans.ttf', name: 'Open Sans'},
      {id: 'Roboto.ttf', name: 'Roboto'},
      {id: 'Lato.ttf', name: 'Lato'}
    ];
    $scope.info = {wmt: $scope.wmtOptions[0].id, wmp: $scope.wmpOptions[0].id, font: $scope.fontsOptions[0], fontSize: 24};
    $scope.info.txt = 'http://iedit.xxicon.com';
    $scope.info.fontColor = '#333333';
    // $scope.imagePath = '';
    $scope.refreshImage('image');
    $scope.refreshImage('mark');
    angular.element('.cls-file-upload').fileupload({
      add: function (e, data) {
        data.submit();
      },
      done: function (e, data) {
        $scope.afterUpload(data.result);
        var category = data.category;
        if (category == 'image') {
          clearImagePath($scope.wmtOptions[0].id);
          clearImagePath($scope.wmtOptions[1].id);
        } else {
          clearImagePath($scope.wmtOptions[1].id);
        }
        $scope.$apply();
      }
    });
    var refreshImage = function () {
      $scope.imagePath = $scope.getImgCookies('watermark-' + $scope.info.wmt + '-' + $scope.info.wmp);
    };
    var clearImagePath = function (type) {
        if (!type) {
          type = $scope.info.wmt;
        }
        for (var i=0; i<$scope.wmpOptions.length; i++) {
          $scope.removeImgCookies('watermark-' + type + '-' + $scope.wmpOptions[i].id);
        }
        $scope.imagePath = '';
    };
    $scope.changeWMType = function () {
      $scope.info.isTxtType = $scope.info.wmt == $scope.wmtOptions[0].id;
      refreshImage();
    };
    $scope.changeWMPos = function () {
      refreshImage();
    };
    $scope.changeWMType();
    $scope.changeTxtFont = function () {
      refreshImage();
    };
    $scope.btnWaterMark = function () {
      if (!$scope.image) {
        alert('请上传需要加水印的图片');
        return;
      }
      $log.debug($scope.info);
      var param = {image: $scope.image, type: $scope.info.wmt, pos: $scope.info.wmp};
      if ($scope.info.isTxtType) {
        if (!$scope.info.txt) {
          alert('请填写水印文字');
          return;
        }
        if (!$scope.info.fontSize) {
          alert('请设置水印文字大小');
          return;
        }
        if (!$scope.info.fontColor) {
          alert('请设置水印文字颜色');
          return;
        }
        param.txt = $scope.info.txt;
        param.font = $scope.info.font.id;
        param.fontSize = $scope.info.fontSize;
        param.fontColor = $scope.info.fontColor;
      } else {
        if (!$scope.mark) {
          alert('请上传水印图标');
          return;
        }
        param.mark = $scope.mark;
      }
      $log.debug(param);
      Watermark.get(param, function (data) {
        $log.debug(data);
        if (data.code == 404) {
          $scope.image = '';
          $scope.mark = '';
          $scope.removeImgCookies('image');
          $scope.removeImgCookies('mark');
          clearImagePath(param.type);
          alert('图片已失效，请重新上传！');
          return;
        }
        if (data.code != 200) {
          alert(data.code + ': ' + data.msg);
          return;
        }
        $scope.setImgCookies('watermark-' + param.type + '-' + param.pos, data.fp + '/' + data.fn);
        refreshImage();
      });
    };
  }]);
