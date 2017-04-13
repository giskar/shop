/**
 * Created by troviln on 13.04.17.
 */
angular.module('productApp', [
  'ui.router',
  'ngResource',
  'productApp.services',
  'productApp.controllers'
])
  .config(function ($interpolateProvider, $httpProvider, $resourceProvider, $stateProvider, $urlRouterProvider, $locationProvider) {
    // Force angular to use square brackets for template tag
    // The alternative is using {% verbatim %}
    $interpolateProvider.startSymbol('[[').endSymbol(']]');

    // CSRF Support
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $locationProvider.html5Mode(true);

    // This only works in angular 3!
    // It makes dealing with Django slashes at the end of everything easier.
    $resourceProvider.defaults.stripTrailingSlashes = false;

    // Django expects jQuery like headers
    // $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

     //Routing
    $urlRouterProvider.otherwise('/ang');
    $stateProvider
      .state('products', {
        url: '/ang',
        templateUrl: 'static/js/product-list.html',
        controller: 'ProductCtrl'
      });
    //  .state('profile', {
    //    url: '/profile/',
    //    templateUrl: 'static/partials/profile.html',
    //    controller: 'UserCtrl'
    //  })
    //  .state('product', {
    //    url: '/product/:pr_id/',
    //    templateUrl: 'static/partials/product-detail.html',
    //    controller: 'DetailCtrl'
    //  })
  });
