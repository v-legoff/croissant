.. Introduction to Behavior-Driven Development

What is BDD (Behavior-Driven Development)
=========================================

This document is designed to introduce you to the
Behavior-driven development.  The aim of this document is for people
working in non-technical fields to understand the benefits of this
specific approach without particular knowledges in development.

What is it for?
---------------

One of the most important benefits of the behavior-driven development
approach is to create something (like a new tool) in term of usability.
Let's not talk about creating anything yet.  Let's take a look at
something which already exists: an umbrella.

Define an umbrella
^^^^^^^^^^^^^^^^^^

What's it for?  Well, to be able to go outside when it's raining and
stay in the dry.  It's its main purpose, I think.

To better define a 'purpose', let's try to describe it in three
lines:

* I have something
* In case some event happens
* Then I have a result.

Does it sound easy?

* I have an umbrella
* When it's raining outside
* I won't be wet.

If you tro to apply this logic to most of the objects you know and
daily use, you'll see that it still works.  Mostly.

More complete definition
^^^^^^^^^^^^^^^^^^^^^^^^

But what if we imagine the same thing for an object with multiple
usabilities?  Even a phone (a simple one, with which you can only call
and be called) can't be defined with only three lines:

* I have a phone
* When I pick it up and push some buttons
* Then... then what?

What if it's a wrong number?  What if the line is down?  What if three
buttons have been pushed whereas you have to push seven?  Or ten?

In this case, we have to break the definition into smaller pieces and
be as specific as we can to do it.

* Jean has a phone connected to a working phone line
* And Jill also has a phone connected to a working phone line
* Jean's number is 151-877-999
* When Jill pick up her phone and press 151-877-999
* Then Jean's phone will ring.

We could be even more specific, but you should see the difference.
Our result could not be "then Jean will answer his phone", because
we can't know that.  Perhaps he's not home.  Perhaps he's busy mowing
the grass.  Perhaps he doesn't want to.

Back to the BDD approach
^^^^^^^^^^^^^^^^^^^^^^^^

The Behavior-Driven Development approach is generally not used to create umbrellas, let's admit it.  But it's used to create new tools.  Softwares, web sites, even automatic systems could benefit from it.

Let's take an example: perhaps you have, on your computer, a word processor that lets you create and edit documents.  One simple scenario of this software would be:

* I have the main window opened
* When I click on the 'open' button
* Then a new window will appear, allowing me to select a file.

Once more, it's a simple definition.  But it's all there is to it:
BDD is composed of multiple definitions like this, definitions that
can be written and read by anyone.

Why testing?
------------

One common question is: why testing?  I mean, you know that the
software has got an 'open' button on the main window and that, when
you click on it, you will be able to select a file.  Why else would
an 'open' button be on the main window?

Don't worry, a lot of developers wonder exactly the same thing.  One
answer is that, software development is often a long process.  It
may involve different people.  So when one developer works on a very
small project, he can test it (be sure the 'open' button still works).
If he adds some new functionalities, he will try to make sure none of
the new functionalities break the old ones.  But this would become
more and more difficult as the software grows.

Just imagine the consequences for a software that is widely used by
thousands, perhaps even millions of people.  Its team of developers
works on new functionalities forthe new version.  And when it's
distributed to the users, they realize that one of the new functionality
prevents from using an older one.  Like, I added a converting tool...
but, wait a minute, why can't I open any file?

So here's a solution: testing and, even more, automatic testing.  It
means that the developer writes a test and that this test should still
pass when a new version of the software is released.

But there are two problems with this approach:

* First, the developer has to write the tests.  And he is not the
  best person to do it.  Most of the times, the person who would use
  the software itself would have better ideas about testing than the
  developer, because they use the software, they don't develop it.
* Second, the tests are not often centered around usability: to put
  it another way, they think about "what" but they don't always think
  about "why".  This is fine for developers, because they mostly know
  "why", but users don't.

The BDD approach tries to solve these problems:

* First, the tests are not written by developers, they don't require
  technical knowledges about the software, just about what it should
  do.
* Second, the people who write these tests are more concerned about
  usability.  They don't know (and don't mind) how a thing is done,
  they just want it to be done, to work without errors and still work
  after new releases.

What do these tests look like?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Exactly the way we wrote them earlier: common English (or any other language you want).  Of course it should follow some rules.  The most important one is the construction:

* One or more context definitions (I have)
* One event (something happens)
* One or more consequences (then I have).

The vocabulary is slightly different depending on the tool you're using, but it's the same principles:

* First, we have initial state, a context, a list of things that
  are "assumed"
* Then we have an event
* Then we have one or more results (called postconditions here).

But, in pratical terms, how do I test anything?
-----------------------------------------------

The answer of this question mostly depends on the tool you want to use.  But most of the times:

* You write your tests in a simple file
* A developer (or developer's team) converts these tests into
  understable tests for the computer.

Yes, the developers are involved.  They have to be.  But they create generic tests that you'll be able to use without particular knowledges.  And you will be able to read and write tests without knowing the technical details of the software.

Common questions of developers
------------------------------

Can I write tests too?
^^^^^^^^^^^^^^^^^^^^^^

Of course you can.  If you're part of a team of developers and nobody
will be able to write tests out of your team, you should try to do it
yourself.  Writing tests using a BDD tool like Croissant will still be
a good idea.  For one thing, you will have a better understanding of the
user's approach to your software.  Plus, you may have more feedbacks
if anyone can read your tests (and perhaps improve them).

Is there a step-by-step process describing to use a BDD tool?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most of the time there is and you will be able to find it in the
tool's documentation.  As for Croissant, you will find it on the
:doc:`tutorial <tutorial/index>` page.
