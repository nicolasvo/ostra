<template>
    <div>
        <h2>Words</h2>
        <form>
            <input type="text" v-model="insertion.word" placeholder="Word" required />
            <select v-model="insertion.language">
                <option v-for="language in languages">{{ language }}</option>
            </select>
            <button v-on:click.prevent="insertWord">Add word</button>
        </form>
        <div v-if="insertion.submitted"><h4>Word added!</h4></div>
        <br>
        <form>
            <select v-model="deletion.id">
                <option v-for="id in ids">{{ id }}</option>
            </select>
            <button v-on:click.prevent="deleteRow">Delete row</button>
        </form>
        <div v-if="deletion.deleted"><h4>Word deleted!</h4></div>
        <br>
        <table class="table" border="1">
            <thead>
            <th v-for='col in columns'>{{ col }}</th>
            </thead>
            <tbody>
              <tr v-for="(word, index) in words">
                  <td>{{ index + 1 }}</td>
                  <td v-for="language in languages">{{ word[language] }}</td>
              </tr>
            </tbody>
        </table>

    </div>
</template>

<script>
    export default {
      name: 'Words',
      data() {
        return {
          api: 'http://godforgiveme.zapto.org:8080/words',
          insertion: {
            language: '',
            word: '',
            submitted: false,
          },
          deletion: {
            id: [],
            deleted: false,
          },
          word: {
            word_id: '',
          },
          ids: [],
          words: [],
          languages: ["en", "ru", "es"],
          columns: ["#"].concat(["en", "ru", "es"]),
          map_col: {
            "en": "1",
            "ru": "2",
            "es": "3",
          },
        }
      },

      created() {
        this.$http.get(this.api)
        .then(response => {
          this.words = response.body;
          this.ids = this.words.length;
        })
      },

      methods: {
        getWord: function(word_id) {
          this.$http.get(this.api + '/' + word_id)
          .then(response => {
            this.words.push(response.body);
            this.ids = this.words.length;
          })
        },
        insertWord: function() {
          this.$http.post(this.api, {
            word: this.insertion.word,
            col: this.map_col[this.insertion.language],
          })
          .then(response => {
            this.insertion.submitted = true;
            if (response.ok) {
              this.getWord(this.ids + 1);
            }
          })
          .catch(error => {
            console.log(error);
          });
        },
        deleteRow: function() {
          this.$http.delete(this.api, {
            body: {
              row: this.deletion.id,
            }
          })
          .then(response => {
            this.deletion.deleted = true;
            if (response.ok) {
              this.words.splice(this.deletion.id - 1, 1);
              this.ids = this.words.length;
            }
          })
          .catch(error => {
            console.log(typeof this.deletion.id);
            console.log(error);
          });
        }
      }
    }
</script>
