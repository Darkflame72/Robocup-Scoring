<template>
    <div id="signup">
        <div id="loader" class="fade" :class="{fadeIn: !showFormContents, fadeOut: hideLoader}">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
        </div>
        <div id="successful"  class="fade" :class="{fadeIn: successfulPost}">
            <!-- <h1>congrats, its working, you just chucked something in the db</h1> -->
        </div>
        <div id="successful-message" v-if="successfulPost" class="fade" :class="{fadeIn: successfulPost}">
            <h2>Sign up successful</h2>
        </div>
        <div class="fade" :class="{fade: !showFormContents, fadeIn: showFormContents}">
            <h2>Sign up to Robocup Junior</h2>

            <form @submit.prevent="handleSubmit">
                
                    <label>Full Name</label>
                    <input v-model="name" type="text" required>

                    <label>Email <span class="error" v-if="emailError">{{emailError}}</span></label>
                    <input v-model="email" type="email" required>

                    <label>Phone Number</label>
                    <input v-model="ph_number" type="tel" @keypress="onlyNumberKey">
                    
                    <label>Password <span class="error" v-if="passwordError">{{passwordError}}</span></label>
                    <input v-model="password" type="password" required>

                    <button @click="handleSubmit">{{signUpMessage}}</button>
                
                
            </form>
        </div>
    </div>
    
</template>

<script>
import axios from "axios"
export default {
    data() {
        return {
            successfulPost: false,
            showFormContents: true,
            hideLoader: false,
            name: '',
            email: '',
            ph_number: 0,
            password: '',
            passwordError: '',
            emailError: '',
            signUpMessage: "Sign up"
        }
    },

    methods: {

        // forces only numbers to be typed in input for phone
        onlyNumberKey(evt) {
            evt = (evt) ? evt : window.event;
            var charCode = (evt.which) ? evt.which : evt.keyCode;
            if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
                evt.preventDefault();;
            } else {
                return true;
            }
        },
        
        handleSubmit() {
            // validate password
            this.passwordError = this.password.length > 5 ? 
            '' : " - Must be at least 6 chars long";
            
            // validate email
            const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            this.emailError = re.test(String(this.email).toLowerCase()) ? "" : "Must be a valid email"
            
            if (this.passwordError || this.emailError) {return;}

            // submit post req
            let object = {
                "email": this.email,
                "is_superuser": false,
                "full_name": this.name,
                "phone_number": parseInt(this.ph_number),
                "password": this.password
            }

            let successfulPost;
            axios.post('/api/v1/users', object)
            .then(function (response) {
                console.log(response);
                successfulPost = true;
            })
            .catch(function (error) {
                console.log(error);
                successfulPost = false;
            });

            
            // do the transition thing
            this.showFormContents = false;
            setTimeout(() => {
                this.hideLoader = true;

                // go to signed in page
                if (successfulPost) {
                    this.successfulPost = true;
                } 
                
                // don't go, but go back to form, and display error
                else {
                    this.showFormContents = true;
                    this.signUpMessage = "Error submitting - Click to try again"
                }
            }, 1500)
            
        }
    }
}
</script>

<style>
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

    #loader div {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #8cce7e;
        animation: loader 0.5s cubic-bezier(.19, .57, .3, .98) infinite alternate;
    }

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


    #signup {
        position: relative;
        display: flex;
        flex-direction: column;
        max-width: 420px;
        margin: 30px auto;
        background: #fff;
        text-align: left;
        border: 1px solid #888;
        box-shadow: 5px 5px 10px lightgrey;
        padding: 40px;
        border-radius: 2px;
    }

    #signup h2 {
        text-align: center;
    }

    #signup label {
        color: #aaa;
        display: inline-block;
        margin: 25px 0 15px;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: bold;
    }

    #signup input {
        display: block;
        padding: 10px 6px;
        box-sizing: border-box;
        border: none;
        border-bottom: 1px solid #ddd;
        color: #555;
        margin: 0;
        width: 100%;
        font-size: 1em;
    }

    #signup input:focus {
        outline: none;
        border:none;
        border-bottom: 1px solid #8cce7e;
    }

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

    .error {
        color: crimson;
        text-transform: none;
        font-size: 0.9em;
    }

    .fade {
        transition: 0.5s;
        opacity: 0%;
    }

    .fadeIn {
        opacity: 100% !important;
    }

    .fadeOut {
        opacity: 0% !important;
    }

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
</style>