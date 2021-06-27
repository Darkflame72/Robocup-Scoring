<template>
    <!-- this div is the box that surrounds the whole form -->
    <div id="signup">

        <!-- the hidden components below don't use v-if - so they can fade in -->
        <!-- div that handles the 4 bouncing balls when a submission is made - hidden until !showFormcontents -->
        <div id="loader" class="fade" :class="{fadeIn: !showFormContents, fadeOut: hideLoader}">
            <div></div> <!-- ball div ... -->
            <div></div>
            <div></div>
            <div></div>
        </div>

        <!-- div for the successful green circle + checkmark - hidden until sucessfulPost -->
        <div id="successful"  class="fade" :class="{fadeIn: successfulPost}"></div>

        <!-- the message below the green circle on success - hidden until successfulPost-->
        <div id="successful-message" v-if="successfulPost" class="fade" :class="{fadeIn: successfulPost}">
            <h2>Sign up successful</h2>
        </div>

        <!-- MAIN FORM  -->
        <div class="fade" :class="{fade: !showFormContents, fadeIn: showFormContents}">
            <h2>Sign up to Robocup Junior</h2>

            <!--on button click - do not autosubmit, handle it through vue, handleSubmit()-->
            <form @submit.prevent="handleSubmit">  
                    <label>Full Name</label>
                    <input v-model="name" type="text" required>

                    <label>Email <span class="error" v-if="emailError">{{emailError}}</span></label>
                    <input ref="email" v-model="email" type="text" required>

                    <label>Phone Number</label>
                    <input v-model="ph_number" type="tel" @keypress="onlyNumberKey">
                    
                    <label>Password <span class="error" v-if="passwordError">{{passwordError}}</span></label>
                    <input ref="password" v-model="password" type="password" required>

                    <button :class="{shake: failedPost}" @click="handleSubmit">{{signUpMessage}}</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios"

export default {
    data() {
        return {
            failedPost: false,          // simply for shake detection - when error or cant POST
            successfulPost: null,       // whether the green checkmark screen is shown
            showFormContents: true,     // whether the main inputs to the form are shown
            hideLoader: false,          // whether the CSS loader is shown
            name: '',                   // mapped with v-model to name input
            email: '',                  // mapped with v-model to email input
            ph_number: 0,               // mapped with v-model to phone number input
            password: '',               // mapped with v-model to password input
            passwordError: '',          // red error next to the password field, shown if error != ''
            emailError: '',             // red error next to the email field, shown if error != ''    
            signUpMessage: "Sign up"    // controls message in the button
        }
    },

    methods: {
        /**
         * Forces all recorded presses to be numeric only in the phone number input
         */
        onlyNumberKey(evt) {
            evt = (evt) ? evt : window.event;
            var charCode = (evt.which) ? evt.which : evt.keyCode;
            if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
                evt.preventDefault();;
            } else {
                return true;
            }
        },
        
        /**
         * Handles the submit request from the form button press, sanitising, POST to server, transition to next page
         */
        handleSubmit() {
            // Reset shake attribute
            this.failedPost = false;

            // Raise error if password is not at least 6 chars
            let minPasswordLength = 6
            this.passwordError = this.password.length >= minPasswordLength ? 
            '' : " - Must be at least 6 chars long";
            
            // Raise error if email does not match email regex
            const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            this.emailError = re.test(String(this.email).toLowerCase()) ? "" : "Must be a valid email"
            
            // Do not continue with POST request if either errors detected
            if (this.emailError) {
                this.$refs.email.focus();
                return;
            } else if (this.passwordError) {
                this.$refs.password.focus();
                return;
            }

            // Package to submit
            let object = {
                "email": this.email,
                "is_superuser": false,
                "full_name": this.name,
                "phone_number": parseInt(this.ph_number),
                "password": this.password
            }

            // This variables records whether the submission was successful or not
            let successfulPost;

            // POST request with axios
            axios.post('/api/v1/users', object)
            .then(function (response) {
                successfulPost = true;
            })
            .catch(function (error) {     // what to do in error
                successfulPost = false;
            });

            
            // Hide the form contents and display the loader
            this.showFormContents = false;
            this.hideLoader = false;
            setTimeout(() => {
                this.hideLoader = true;

                // If successful submission to the database - show checkmark
                if (successfulPost) {
                    this.successfulPost = true;
                } 
                
                // If failure, show form again, with an error message on the green button
                else {
                    this.showFormContents = true;
                    this.failedPost = true;
                    this.signUpMessage = "Error submitting - Click to try again"
                }

            }, 1500) // Number = time to show loader for (yes i know its hardcoded lmao)
        }
    }
}
</script>

<style scoped src="../assets/SignupForm.css"></style>