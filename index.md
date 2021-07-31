---
layout: default
---

# About Me

Software Engineer (actual one, by French standard) with a Master's Degree in Computer Science.
Technology enthusiast with 20+ years of experience in developing software solutions in different industries like travel, education, and healthcare, in a startup environment.

I code software on my (really small) spare time to scratch an itch, learn something new, investigate new architectures and solutions, and give back to the open source community. 


# Projects

## United File Service (not open source)

Simple and secure way to exchange files, small and big. Pay only for what you need.
The idea was to develop a production-grade serverless service around simple file drop with notifications and third party payment processing.

<img src="./assets/images/unitedfileservice.png" alt="Typescript" width="200"/>

This service is available at [unitedfileservice.com](https://unitedfileservice.com/).

## <img src="./assets/images/typescript-programming-language.svg" alt="Typescript" width="30"/> ETL-JS / ETL-JS-CLI

Extract, Transform, and Load sharable and repeatable from command line.
The idea came from trying to script ETL by leveraging existing tools (mysql, ssh, etc.).

```yaml
# ==================================================================================
# mysqlimports eample
# ==================================================================================

etlSets:
  default:
    - extract
    - load

# ==================================================================================
# Create test data
# ==================================================================================
extract:
  files:
    "/tmp/station_prcp_snow.csv":
      content: |
        [SomethngToIgnore]
        "station_id","prcp","snow"
        "US1",123,456
        "US2",234,345
        "US3",345,567

# ==================================================================================
# Load data into MySQL DB
# ==================================================================================
load:
  mysqlimports:
    "/tmp/test.csv":
      db_name: testdb
      columns: "station_id,prcp,snow"
      fields_terminated_by: ","
      lines_terminated_by: "\\n"
      fields_enclosed_by: '"'
      ignore_lines: 2
      delete: true
```
Here's another concrete example [Processing and graphing out precipitation and snowfall for specific weather stations.](https://github.com/lpezet/etl-js-cli/blob/master/examples/prcp_snow_chart.yml).

You can find more details at [etl-js](https://github.com/lpezet/etl-js) and [etl-js-cli](https://github.com/lpezet/etl-js-cli).

## <img src="./assets/images/typescript-programming-language.svg" alt="Typescript" width="30"/> MKay Diary

Simple NodeJS package providing command line interface to easily create and edit diary entries for development and more.

```bash
mkay-diary entry # to create or edit today's entry
mkay-diary full # to create full diary
mkay-diary embed # to embed full diray in Readme.md
```

The goal of this tool is to help generate and integrate a simple dev diary. Working on lots of small projects, I found it useful to keep a diary, with simple daily entries. For example, going back to those entries after long periods of coding idleness helps remember where things were left off. Other times, without being away too long, it helps reading through a train a thought written down.

You can find more details at [mkay-diary](https://github.com/lpezet/mkay-diary).

## <img src="./assets/images/cmd-terminal.svg" alt="Command" width="30"/> AWS MFA

Simple bash script to help use MFA with AWS CLI.
It leverages aws cli to store your new session information in your aws cli configuration. You can then reference your new profile in further aws cli commands.

```bash
aws-mfa someprofile 123456 # OTP from your device
aws --profile someprofile-mfa s3 cp ... # use your -mfa new temporary credentials now
```

You can find more details at [aws-mfa](https://github.com/lpezet/aws-mfa).

## <img src="./assets/images/javascript-programming-language.svg" alt="Javascript" width="30"/> King

Named after the Kong Inc. company, this is a little research project into rate-limiting, which Kong provides [here](https://docs.konghq.com/hub/kong-inc/rate-limiting/#enabling-the-plugin-on-a-service).

```
X-RateLimit-Limit-minute: 10
X-RateLimit-Remaining-minute: 0
X-RateLimit-Remaining-minute-Reset: 51624
X-RateLimit-Limit-day: 100
X-RateLimit-Remaining-day: 77
```

The goal was to implement simple rate limiting using some technology (redis) in Javascript and figure out its cost model.

The can find more details at [king](https://github.com/lpezet/king).

## <img src="./assets/images/typescript-programming-language.svg" alt="Typescript" width="30"/> Cue Me In (in progress)

This project is to simplify user notifications. An app is provided and users (developers) can leverage CueMeIn to detect changes and trigger notifications.
The goal of this project was to first look into authentication/oauth integration with CLI programs (creating local server for callback), serverless functions (Google Functions or AWS Lambda), and managed user base (e.g. Firebase).

You can find more details at [cue-me-in-cli](https://github.com/lpezet/cue-me-in-cli).

## <img src="https://avatars.githubusercontent.com/u/900867?s=30&v=4" alt="HPCCSystems"/> HPCCSystems ECL Bundle

This project regroups some functionality I often use when working with data using HPCC Systems platform.

```ecl
IMPORT LPezet.Linux.Curl;

Curl.download( 'ftp://ftp.fu-berlin.de/pub/misc/movies/database/actresses.list.gz', '/tmp/actresses.list.gz' );

oFiles := DATASET([ {'ftp://ftp.fu-berlin.de/pub/misc/movies/database/actors.list.gz', '/tmp/actors.list.gz', false}, {'ftp://ftp.fu-berlin.de/pub/misc/movies/database/actresses.list.gz', '/tmp/actresses.list.gz', false}, {'ftp://ftp.fu-berlin.de/pub/misc/movies/database/directors.list.gz', '/tmp/directors.list.gz', false}], Curl.batch_layout );
Curl.batch_download( oFiles );
```

You can find more details at [ecl-bundle-lpezet](https://github.com/lpezet/ecl-bundle-lpezet).

## <img src="./assets/images/java-programming-language.svg" alt="Java" width="30"/> Java Patterns, BufferedIterator, ...

A collection of classes and logic, like circuit breaker, I ended up reusing a lot at work and on other personal projects.

```java
public class SingleTryCircuitBreakerStrategyTest {

	@Test(expected=CircuitBreakerOpenException.class)
	public void stillOpen() throws Exception {
		SingleTryCircuitBreakerStrategy oStg = new SingleTryCircuitBreakerStrategy();
		oStg.setOpenToHalfOpenWaitTimeInMillis(500);
		ICircuitBreaker oBreaker = Mockito.mock(ICircuitBreaker.class);
		when(oBreaker.getLastStateChangedDateUTC()).thenReturn(DateTime.now());
		oStg.handleOpen(oBreaker, null);
	}
	
	@Test
	public void openToHalfOpenToClosed() throws Exception {
		SingleTryCircuitBreakerStrategy oStg = new SingleTryCircuitBreakerStrategy();
		oStg.setOpenToHalfOpenWaitTimeInMillis(500);
		ICircuitBreaker oBreaker = Mockito.mock(ICircuitBreaker.class);
		when(oBreaker.getLastStateChangedDateUTC()).thenReturn(DateTime.now().minusDays(1));
		Callable oCallable = Mockito.mock(Callable.class);
		when(oCallable.call()).thenReturn("HELLO");
		oStg.handleOpen(oBreaker, oCallable);
		verify(oBreaker, times(1)).halfOpen();
		verify(oBreaker, times(1)).reset();
	}
	
	@Test(expected=IOException.class)
	public void openToHalfOpen() throws Exception {
		SingleTryCircuitBreakerStrategy oStg = new SingleTryCircuitBreakerStrategy();
		oStg.setOpenToHalfOpenWaitTimeInMillis(500);
		ICircuitBreaker oBreaker = Mockito.mock(ICircuitBreaker.class);
		when(oBreaker.getLastStateChangedDateUTC()).thenReturn(DateTime.now().minusDays(1));
		Callable oCallable = Mockito.mock(Callable.class);
		when(oCallable.call()).thenThrow(new IOException());
		try {
			oStg.handleOpen(oBreaker, oCallable);
		} finally {
			verify(oBreaker, times(1)).halfOpen();
			verify(oBreaker, never()).reset();
			verify(oBreaker, times(1)).trip(any(Exception.class));
		}
	}
}
```

You can find more details at [java](https://github.com/lpezet/java).

## More

I worked on lots of projects, from SAS port to ECL, to Unreal Engine 4 shoot-them-up. I always strive to complete my projects, but there is only 24 hours in a day.

You can find more at [lpezet](https://github.com/lpezet).


[ts-image]: ./assets/images/typescript-programming-language.svg
[js-image]: ./assets/images/javascript-programming-language.svg
[java-image]: ./assets/images/java-programming-language.svg
[cmd-image]: ./assets/images/cmd-terminal.svg
