import React, {useState} from 'react'
import axios from 'axios'
import '../css/main.css'

function TopBar(props) {

    const [userEntry, setUserEntry] = useState("")

    function setUser(e) {
        e.preventDefault()
        if (userEntry.length < 3) {
            alert("Username must be longer than 2 characters.")
        } else {
            const data = {
                'command': 'CHECKUSER',
                'userid': userEntry
            }
            axios.post('http://localhost:81/', data).
                then((response) => {
                    console.log("Setting user: " + userEntry)
                    console.log(response.data)
                    props.setUser(userEntry)
                    props.setInfo(response.data.result)
                }, (error) => {
                    alert(error)
                })
            
            setUserEntry("")
        }
    }

    function handleChange(event) {
        setUserEntry(event.target.value)
    }

    return (
        <div className="bar">
            <div className="topTitle">Stocker Strange</div>
            <form onSubmit={setUser}>
                <input type="text" className="topInput" onChange={handleChange} value={userEntry} placeholder="Enter username..."></input>
                <input type="submit" className="topButton" value="log in"></input>
            </form>
        </div>
    )
}

export default TopBar