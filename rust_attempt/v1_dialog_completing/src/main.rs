use lambda_http::{run, service_fn, Body, Error, Request, Response};
use async_openai::{
    types::{ChatCompletionRequestMessageArgs, CreateChatCompletionRequestArgs, Role},
    Client,
};
// use serde_json::{json};
use tbot::prelude::*;
use tbot::types::user::Id as UserChatId;


fn generate_main_user_message(messages: &[Message; 3]) -> String {
    let mut final_message = String::from(
        "Напиши повідомлення довжиною від 5 до 40 слів у продовження до бесіди :\n"
    );
    for msg in messages.iter() {
        final_message += format!("{}:\n{}\n\n", msg.username, msg.text).as_str();
    }
    final_message
}

struct Message {
    username: String,
    text: String,
}

async fn function_handler(event: Request) -> Result<Response<Body>, Error> {
    let client = Client::new();

    // let messages = json!(
    //     [
    //         {
    //             "username": "Сашко",
    //             "text": "Єбать\nЗнаєте, шо я зрозумів?\n\
    //                     Хлорофіл - це...... Той, хто любить (або навіть трахає) хлор 😳😳"
    //         },
    //         {
    //             "username": "Борис",
    //             "text": "Тільки тут хлор не в значенні газу, в значенні \"зелений\""},
    //         {
    //             "username": "Влад",
    //             "text": "Слонік"
    //         }
    //     ]
    // );
    let messages = [
        Message {
            username: "Сашко".to_string(),
            text: "Єбать\nЗнаєте, шо я зрозумів?\n\
                  Хлорофіл - це...... Той, хто любить (або навіть трахає) хлор 😳😳".to_string()
        },
        Message {
            username: "Борис".to_string(),
            text: "Тільки тут хлор не в значенні газу, в значенні \"зелений\"".to_string()
        },
        Message {
            username: "Влад".to_string(),
            text: "Слонік".to_string()
        }
    ];

    // let request = CreateChatCompletionRequestArgs::default()
    //     .max_tokens(125_u16)
    //     .model("gpt-4")
    //     .temperature(0.7_f32)
    //     .messages([
    //         ChatCompletionRequestMessageArgs::default()
    //             .role(Role::System)
    //             .content(
    //                 "Act as a member of the friends group chat. \
    //                 You are a freaky, funny, and interesting companion. \
    //                 You like to says crazy things, \
    //                 which surprise and amuse your friends using swearing sometimes. \
    //                 You are rude a little."
    //                 // You love Ukraine, hate Russia and Putin. Sometimes you use ."
    //                 // #TODO finish
    //             )
    //             .build()?,
    //         ChatCompletionRequestMessageArgs::default()
    //             .role(Role::User)
    //             .content(generate_main_user_message(&messages))
    //             .build()?
    //     ])
    //     .build()?;
    //
    // let response = client.chat().create(request).await?;
    // let resp = Response::builder()
    //     .status(200)
    //     .body(response.choices[0].message.content.clone().into())
    //     .map_err(Box::new)?;
    let resp = Response::builder()
        .status(200)
        .body("OK".into())
        .map_err(Box::new)?;


    let mut bot = tbot::Bot::from_env("TELEGRAM_BOT_TOKEN");

    bot.send_message(UserChatId(355526766), "Hello world!").call().await.unwrap();
    // bot.polling().start().await.unwrap();
    Ok(resp)
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::INFO)
        .with_target(false)
        .without_time()
        .init();

    run(service_fn(function_handler)).await
}
