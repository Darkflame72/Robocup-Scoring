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
                    <input ref="email" v-model="email" type="email" required>

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
            failedPost: false,          // simply for shake detection
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
                this.failedPost = true;
                return;
            } else if (this.passwordError) {
                this.$refs.password.focus();
                this.failedPost = true;
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

<style>

    /* bouncing balls wrapper */
    #loader {
        transition: 1s;
        opacity: 0;
        height: 100px;
        width: 130px;
        background: #fff;
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        margin: auto;
        display: flex;
        justify-content: space-around;
        align-items: flex-end;
    }
        /* individual bouncing balls */
        #loader div {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #8cce7e;
            animation: loader 0.5s cubic-bezier(.19, .57, .3, .98) infinite alternate;
        }

        /* staggering of the bouncing balls */
        #loader div:nth-child(2) {
            animation-delay: 0.1s;
            opacity: 0.8;
        }

        #loader div:nth-child(3) {
            animation-delay: 0.2s;
            opacity: 0.6;
        }

        #loader div:nth-child(4) {
            animation-delay: 0.4s;
            opacity: 0.4;
        }
        
        @keyframes loader {
            from {
                transform: translateY(0);
            }
            to {
                transform: translateY(-30px);
            }
        }

    /* the wrapper for the whole form  */
    #signup {
        position: relative;
        display: flex;
        flex-direction: column;
        max-width: 420px;             /* change fixed width of form */
        margin: 30px auto;
        background: #fff;
        text-align: left;
        border: 1px solid #888;
        box-shadow: 5px 5px 10px lightgrey;
        padding: 40px;
        border-radius: 2px;
    }
        /* title for the form ("sign up to robocup") thing */
        #signup h2 {
            text-align: center;
        }

        /* the messages above the inputs */
        #signup label {
            color: #aaa;
            display: inline-block;
            margin: 25px 0 15px;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: bold;
        }

        /* the user input css */
        #signup input {
            z-index: 1;
            display: block;
            padding: 10px 6px;
            box-sizing: border-box;
            border: 0;
            border-bottom: 1px solid #ddd;
            color: #555;
            margin: 0;
            width: 100%;
            font-size: 1em;
            cursor: pointer;
        }

        #signup input:focus {
            outline: none;
            border:none;
            border-bottom: 1px solid #8cce7e;
        }

        /* button at the bottom of the form */
        #signup button {
            display: inline-block;
            background: #52a740;
            border: 0;
            padding: 10px 20px;
            margin-top: 40px;
            color: white;
            border-radius: 20px;
            width: 100%;
            cursor: pointer;
        }

    /* what to style error messages as, above the inputs, next to labels */
    .error {
        color: crimson;
        text-transform: none;
        font-size: 0.9em;
    }

    /* hides element, and when you apply .fadeIn, it fades in */
    .fade {
        transition: 0.5s;
        opacity: 0%;
    }

    .fadeIn {
        opacity: 100% !important;
    }

    /* when applied to an element with fade, it will go back to hidden */
    .fadeOut {
        opacity: 0% !important;
    }

    /* css for the green checkmark */
    #successful {
        z-index: 1;
        position: absolute;
        width: 200px;
        height: 200px;
        background: #7cc76d;
        margin: auto;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        margin: auto;
        border-radius: 50%;    
    }

    #successful:after {
        content: " ";
        display: block;
        width: 0.3em; 
        height: 0.6em;
        border: solid white;
        border-width: 0 0.2em 0.2em 0; 
        position: absolute;
        left: 95px;
        top: 45%;
        margin-top: -0.2em;
        -webkit-transform: rotate(45deg);
        -moz-transform: rotate(45deg);
        -o-transform: rotate(45deg);
        transform: rotate(45deg) scale(5);
    }

    /* css for the message below the checkmark */
    #successful-message {
        z-index: 1;
        position: absolute;
        left: 0;
        right: 0;
        top: 70%;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9em;
        color: rgba(0,0,0, 0.8);
    }

    /* shake image */
    /* https://www.w3schools.com/howto/howto_css_shake_image.asp */
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(3px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(3px, 1px) rotate(-1deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        90% { transform: translate(1px, 2px) rotate(0deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }

    .shake {
        animation: 0.5s shake;
    }

</style>