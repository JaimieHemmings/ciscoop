# Testing Documentation

![Preview of Website](documentation/img/preview.jpg)

# Validation Results

## W3C Markup Validator Results

- [Homepage](https://validator.w3.org/nu/?doc=https%3A%2F%2Fciscoop-46d70b5281a0.herokuapp.com%2F)
- [Blog Page](https://validator.w3.org/nu/?doc=https%3A%2F%2Fciscoop-46d70b5281a0.herokuapp.com%2Fblog)
- [Article Page](https://validator.w3.org/nu/?doc=https%3A%2F%2Fciscoop-46d70b5281a0.herokuapp.com%2Fblog%2Fthe-future-of-software-development)
- [Contact Page](https://validator.w3.org/nu/?doc=https%3A%2F%2Fciscoop-46d70b5281a0.herokuapp.com%2Fcontact)
- [Login Page](https://validator.w3.org/nu/?doc=https%3A%2F%2Fciscoop-46d70b5281a0.herokuapp.com%2Flogin)
- [Register Page](https://validator.w3.org/nu/?doc=https%3A%2F%2Fciscoop-46d70b5281a0.herokuapp.com%2Fregister)

## W3c CSS Validator

- [CSS Validation results](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fciscoop-46d70b5281a0.herokuapp.com%2Findex&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)

As seen by the results, I have no errors in my CSS, although I do have warnings for the case of CSS Variables not being checked. The warning about CSS Variables is the overwhelming majority of the warnings with several others being for vendor prefixes. Additionally, these errors are coming from the Bootstrap 5 stylsheets which I have no direct control over.

![CSS Validation](https://jigsaw.w3.org/css-validator/images/vcss-blue)

## JSHint Results

My Javascript file is particularly small but for the sake of completeness I have included a JSHint testing of the file. The results of which are below.

![JSHint Results](documentation/img/js-hint-results.png)

## PEP8 Validation

![PEP8 Validation](documentation/img/pep8-validator.png)

## Lighthouse Results

- [Home - Mobile](documentation/lighthouse-results/home-mobile.png)
- [Home - Desktop](documentation/lighthouse-results/home-desktop.png)
- [Blog - Mobile](documentation/lighthouse-results/blog-mobile.png)
- [Blog - Desktop](documentation/lighthouse-results/blog-desktop.png)
- [Article - Mobile](documentation/lighthouse-results/article-mobile.png)
- [Article - Desktop](documentation/lighthouse-results/article-desktop.png)
- [Contact - Mobile](documentation/lighthouse-results/contact-mobile.png)
- [Contact - Desktop](documentation/lighthouse-results/contact-desktop.png)

## a11y Contrast Test Results

![a11y Contrast Results](documentation/a11y-results/a11y-results.png)

The a11y Contrast Test results displayed one issue which I believe is a false positive, as it is showing black text on a black background for the text "FRONTEND" which I believe to be the section shown in the picture below.

![False Positive](documentation/a11y-results/false-positive.png)

As you can see the text is actually white. It has a hover state where the background is red and the text is black so I believe the automated testing has somehow gotten confused so i will be ignoring this error.
