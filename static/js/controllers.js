var productControllers = angular.module('productApp.controllers', []);

productControllers.controller('ProductCtrl', function ProductCtrl($scope, Product) {
  $scope.products = {};

  Product.get(function (response) {
    $scope.products = response.objects;
  });
});


//productControllers.controller('UserCtrl', function UserCtrl($scope, Product, User, AuthUser) {
//  $scope.products = {};
//  id = AuthUser.id;
//  User.get({id:id}, function(response) {
//    $scope.user = response;
//    $scope.products = response.products;
//  });
//
//});
//
//
//productControllers.controller('DetailCtrl', function DetailCtrl($scope,$stateParams,Product)
//{
//
//  Product.get({id:$stateParams.pr_id}, function(response) {
//    $scope.product = response;
//  });
//
//
//
//
//});